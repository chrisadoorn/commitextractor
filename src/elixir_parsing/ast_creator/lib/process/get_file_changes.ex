defmodule AstCreator.GetFileChanges do
  use GenServer

  @moduledoc """
    This module will run as a single proces,
    it will get all ids from bestandswijziging and puts this in a queue.
    Client processes may pop a value from this list
    This ensures all ids are processed and no ids are double processed.
    This module is similar to GetFileChangesWithoutTokens
  """

  @doc """
    This method will deliver all bestandswijziging ids without a abstract_syntax_trees
    record
  """
  def get_ids() do
    query =
      """
      select bw.id from v11.bestandswijziging bw
      left join v11.abstract_syntax_trees a on bw.id = a.bestandswijziging_id
      where a.id is null  order by bw.id asc;
      """

    Ecto.Adapters.SQL.query(AstCreator.Repo, query, [])
  end

  @doc """
    start a process, initialises the state with a queue of ids
  """
  def start_link(_) do
    IO.puts("starting main")
    {:ok, x} = get_ids()
    IO.puts(x.num_rows)
    GenServer.start_link(__MODULE__, x.rows, name: __MODULE__) # starts a recursive loop inside genserver
  end

  @doc """
    callback that will be called from genserver to initialise proces.
  """
  @impl true
  def init(list) do
    {:ok, list} # list is the initial state
  end

  @doc """
    -callback that handles a call with atom :pop, replies with head, keeps tail as state
    -tail is the new state
    -functions are selected by pattern matching
    -next handles the empty queue
  """
  @impl true
  def handle_call(:pop, _from, [head | tail]) do
    {:reply, head, tail}
  end


  @impl true
  def handle_call(:pop, _from, _) do
    {:reply, nil, nil}
  end

  @doc """
    -callback that adds an element to the front of a queue
    -[element | state] is new state
  """
  @impl true
  def handle_cast({:push, element}, state) do
    {:noreply, [element | state]}
  end

  @doc """
    -sends a call with a atom :pop to this module
  """
  def next_filechange() do
    GenServer.call(__MODULE__, :pop)
  end
end
