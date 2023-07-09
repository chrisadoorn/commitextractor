defmodule AstCreator.MakeAst do
  use GenServer
  import Ecto.Query, only: [from: 2]

  def start(name_process) do
    IO.puts("starting main")
    GenServer.start(__MODULE__, name_process)
  end

  @impl true
  def init(name_process) do
    AstCreator.Main.get_next(self())
    {:ok, %{:name => name_process, :value => 0}}
  end


  @impl true
  def handle_cast({:nextid, id}, state) do
    IO.puts(Map.get(state, :name))
    IO.inspect(id)
    bestands_wijziging = get_bw_by_id(id)
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
    AstCreator.Main.get_next(self())
    state = %{:name => Map.get(state, :name), :value => next_id}
    {:noreply, state}
  end

  def cast(pid, {:nextid, id}) do
    GenServer.cast(pid, {:nextid, id})
  end

  def get_bw_by_id(id) do
    [h|_] = id
    AstCreator.Repo.get(AstCreator.Bestandswijziging, h)
  end

  defp getAstString(tekst) do
    case tekst do
      nil ->
        nil

      _ ->
        case Code.string_to_quoted(tekst, [unescape: false ]) do
          {:ok, ast} -> inspect(ast, limit: :infinity)
          {:error, {line, error, token}} -> "syntax error, " <> inspect({line, error, token})
        end
    end
  end

  def saveAst(tree) do
    AstCreator.Repo.insert(tree)
  end

end