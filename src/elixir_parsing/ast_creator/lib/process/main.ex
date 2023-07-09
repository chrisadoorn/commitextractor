defmodule AstCreator.Main do
  use GenServer

  def get_ids() do
    query =
      """
      select bw.id from v10.bestandswijziging bw
      left join v10.abstract_syntax_trees_v1 a on bw.id = a.bestandswijziging_id
      where a.id is null order by bw.id asc;
      """
    Ecto.Adapters.SQL.query(AstCreator.Repo, query, [])
  end

  def start() do
    IO.puts("starting main")
    {:ok, x} = get_ids()
    GenServer.start(__MODULE__, x.rows, name: __MODULE__)


    p1 = AstCreator.MakeAst.start("p1")
    p2 = AstCreator.MakeAst.start("p2")
    p3 = AstCreator.MakeAst.start("p3")
    p4 = AstCreator.MakeAst.start("p4")
    p5 = AstCreator.MakeAst.start("p5")
    p6 = AstCreator.MakeAst.start("p6")
    p7 = AstCreator.MakeAst.start("p7")
    p8 = AstCreator.MakeAst.start("p8")
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
  def handle_cast({:push, element}, state) do
    {:noreply, [element | state]}
  end

  def get_next(pid) do
    x =GenServer.call(__MODULE__, :pop)
    AstCreator.MakeAst.cast(pid, {:nextid, x})
  end













end