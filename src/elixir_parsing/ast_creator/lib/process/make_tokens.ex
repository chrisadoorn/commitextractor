defmodule AstCreator.MakeTokens do
  use GenServer

  def start_link({worker_id}) do
    str = to_string(worker_id)
    IO.inspect("start makeTokens #{str}")
    GenServer.start_link(__MODULE__, worker_id,name: via_tuple(worker_id))
  end

  @impl true
  def init(worker_id) do
    get_next(worker_id)
    {:ok, %{:name => worker_id, :value => 0}}
  end

  @impl true
  def handle_cast({:nextid, [id|_]}, state) do
    IO.puts("next id")
    IO.puts(id)
    bestands_wijziging = get_bw_by_id(id)
    abstract_syntax_tree = get_ast_by_id(id)
    if bestands_wijziging != nil and abstract_syntax_tree != nil do
      IO.puts("bw opgehaald")
      IO.puts("ast opgehaald")
      IO.puts(bestands_wijziging.id)
      abstract_syntax_tree  = Ecto.Changeset.change(abstract_syntax_tree,
      %{tekstvooraf_tokens: getTokenString(bestands_wijziging.tekstvooraf), tekstachteraf_tokens: getTokenString(bestands_wijziging.tekstachteraf)})
      updateAst(abstract_syntax_tree)
    end

    next_id = id
    get_next(Map.get(state, :name))
    state = %{:name => Map.get(state, :name), :value => next_id}
    {:noreply, state}
  end

  @impl true
  def handle_cast({:noid, _}, state) do
    {:noreply, state}
  end

  def cast(pid, {:nextid, id}) do
    GenServer.cast(pid, {:nextid, id})
  end

  def cast(pid, {:noid, _}) do
    GenServer.cast(pid, {:noid, nil})
  end


  def get_bw_by_id(id) do
    AstCreator.Repo.get(AstCreator.Bestandswijziging, id)
  end

  def get_ast_by_id(id) do
    AstCreator.Repo.get_by(AstCreator.AbstractSyntaxTree, bestandswijziging_id: id)
  end

  def getTokenString(tekst) do
    case tekst do
      nil -> nil
      _ ->
        charlist = to_charlist(tekst)
        case :elixir_tokenizer.tokenize(charlist,1,1,[]) do
          {_, _, _, _, e} -> inspect(e, limit: :infinity)
        end
    end
  end

  def updateAst(tree) do
    IO.puts("called update")
    AstCreator.Repo.update(tree)
  end

  def get_next(worker_id) do
    x = AstCreator.GetFileChangesWithoutTokens.next_filechange()
    if x != nil do
      cast(via_tuple(worker_id), {:nextid, x})
    else
      cast(via_tuple(worker_id), {:noid, x})
    end
  end

  defp via_tuple(worker_id) do
    AstCreator.ProcessRegistry.via_tuple({__MODULE__, worker_id})
  end


end
