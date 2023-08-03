defmodule AstCreator.GetFileChanges do
  use GenServer

  def get_ids() do
    query =
      """
      select bw.id from v11.bestandswijziging bw
      left join v11.abstract_syntax_trees a on bw.id = a.bestandswijziging_id
      where a.id is null  order by bw.id asc;
      """

    Ecto.Adapters.SQL.query(AstCreator.Repo, query, [])
  end

  def start_link(_) do
    IO.puts("starting main")
    {:ok, x} = get_ids()
    GenServer.start_link(__MODULE__, x.rows, name: __MODULE__)
  end

  @impl true
  def init(list) do
    {:ok, list}
  end

  @impl true
  def handle_call(:pop, _from, [head | tail]) do
    {:reply, head, tail}
  end

  @impl true
  def handle_call(:pop, _from, _) do
    {:reply, nil, nil}
  end

  @impl true
  def handle_cast({:push, element}, state) do
    {:noreply, [element | state]}
  end

  def next_filechange() do
    GenServer.call(__MODULE__, :pop)
  end
end
