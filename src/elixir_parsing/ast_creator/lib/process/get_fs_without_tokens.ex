defmodule AstCreator.GetFileChangesWithoutTokens do
  use GenServer

  @moduledoc """
    This module will run as a single proces,
    it will get all ids from bestandswijziging and puts this in a queue.
    Client processes may pop a value from this list
    This ensures all ids are processed and no ids are double processed.
    This module should be used after GetFileChanges
  """

  @doc """
    This method will deliver all bestandswijziging ids with a joined abstract_syntax_trees
    and no tekstachteraf_tokens or tekstvooraf_tokens
  """
  def get_ids() do
    query =
      """
      select bw.id from v11.bestandswijziging bw
      join v11.abstract_syntax_trees a on bw.id = a.bestandswijziging_id
      where a.tekstachteraf_tokens is null and a.tekstvooraf_tokens is null order by bw.id asc;
      """

    Ecto.Adapters.SQL.query(AstCreator.Repo, query, [])
  end

  def start_link(_) do
    IO.puts("starting main")
    {:ok, x} = get_ids()
    IO.puts(x.num_rows)
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
