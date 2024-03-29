defmodule AstCreator.System do
  use Supervisor
  @nr_processes 30
  def start_link(_) do
    IO.puts("starting system")
    Supervisor.start_link(__MODULE__, nil) # start callback function init(_)
  end

  def init(_) do
    children = [
    AstCreator.ProcessRegistry,
      %{
        id: AstCreator.GetFileChangesWithoutTokens,
        start: {AstCreator.GetFileChangesWithoutTokens, :start_link, [nil]}
      }
    ]

    children = children ++ Enum.map(1..@nr_processes, &worker_spec/1)
    Supervisor.init(children, strategy: :one_for_one)
  end

  defp worker_spec(worker_id) do
    default_worker_spec = {AstCreator.MakeTokens, {worker_id}}
    Supervisor.child_spec(default_worker_spec, id: worker_id)
  end
end
