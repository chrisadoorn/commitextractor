defmodule AstCreator.Worker do
  import Ecto.Query, only: [from: 2]

  def loop(pid, bw_id, nr_processes, max_id) do
    if get_ast_by_id(bw_id) != nil do
      IO.puts("Skipping: " <> Integer.to_string(bw_id))
    else
      IO.puts("Processing: " <> Integer.to_string(bw_id))
      bestands_wijziging = get_bw_by_id(bw_id)
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
    end

    next_bw_id = bw_id + nr_processes

    if next_bw_id <= max_id do
      loop(pid, next_bw_id, nr_processes, max_id)
    else
      send(pid, {"Process done", self()})
    end
  end

  def start(pid, process_id, nr_processes, max_id) do
    spawn(fn ->
      IO.puts("Starting worker: " <> Integer.to_string(process_id))
      loop(pid, process_id, nr_processes, max_id)
    end)
  end

  def get_bw_by_id(id) do
    AstCreator.Repo.get(AstCreator.Bestandswijziging, id)
  end

  def get_ast_by_id(id) do
    AstCreator.Repo.get_by(AstCreator.AbstractSyntaxTree, bestandswijziging_id: id)
  end

  def get_largest_id() do
    q = from(bw in AstCreator.Bestandswijziging, select: max(bw.id))
    AstCreator.Repo.one(q)
  end

  defp getAstString(tekst) do
    case tekst do
      nil ->
        nil

      _ ->
        case Code.string_to_quoted(tekst, []) do
          {:ok, ast} -> inspect(ast, limit: :infinity)
          {:error, _} -> "syntax error"
        end
    end
  end

  def start_workers() do
    largest_id = get_largest_id()
    IO.puts("Largest id: " <> Integer.to_string(largest_id))
    pids =
      Enum.map(1..32, fn x ->
        start(self(), x, 32, largest_id)
      end)
    keep_going(pids)
  end

  def keep_going(pids) do
    receive do
      message -> IO.inspect(message)
                IO.puts("Received message")
    end

    keep_going(pids)
  end

  def start_link(_) do
    IO.puts("Starting program")
    start_workers()
  end

  def child_spec(opts) do
    %{
      id: __MODULE__,
      start: {__MODULE__, :start_link, [opts]},
      type: :worker,
      restart: :permanent,
      shutdown: 500
    }
  end

  def saveAst(tree) do
    AstCreator.Repo.insert(tree)
  end
end
