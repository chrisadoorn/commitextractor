defmodule AstCreator.MakeAst do
  use GenServer
  import Ecto.Query, only: [from: 2]

  def start_link(worker_id) do
    GenServer.start_link(__MODULE__, worker_id,name: via_tuple(worker_id))
  end

  @impl true
  def init(worker_id) do
    get_next(worker_id)
    {:ok, %{:name => worker_id, :value => 0}}
  end

  @impl true
  def handle_cast({:nextid, id}, state) do
    bestands_wijziging = get_bw_by_id(id)
    IO.inspect(id)

    if bestands_wijziging != nil do
      %AstCreator.AbstractSyntaxTree{
        bestandswijziging_id: bestands_wijziging.id,
        tekstvooraf: bestands_wijziging.tekstvooraf,
        tekstachteraf: bestands_wijziging.tekstachteraf,
        difftext: bestands_wijziging.difftext,
        tekstvooraf_ast: getAstString(bestands_wijziging.tekstvooraf),
        tekstachteraf_ast: getAstString(bestands_wijziging.tekstachteraf)
      }
      |> saveAst
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
    [h | _] = id
    AstCreator.Repo.get(AstCreator.Bestandswijziging, h)
  end

  defp getAstString(tekst) do
    case tekst do
      nil ->
        nil

      _ ->
        case Code.string_to_quoted(tekst, unescape: false) do
          {:ok, ast} -> inspect(ast, limit: :infinity)
          {:error, {line, error, token}} -> "syntax error, " <> inspect({line, error, token})
        end
    end
  end

  def saveAst(tree) do
    AstCreator.Repo.insert(tree)
  end


  def get_next(worker_id) do
    x = AstCreator.Main.call()
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
