defmodule AstCreator.MakeAst do
  use GenServer
  @moduledoc """
  This modules can be used to create a process that retreives a record from
  the database containing a field with Elixix sourcecode.
  It will use the method Code.string_to_quoted to create an AST,
  this AST will be saved in the database.
  Also when an AST can not be created an error message will be saved
  """

  @doc """
    Method to start a process based on this module.
    explanation: name: via_tuple(worker_id) stands for:  name: {:via, Registry, {AstCreator.ProcessRegistry, worker_id}}
    this means the processid can be found by that name, the PID does not have to be saved in the state
  """
  def start_link({worker_id}) do
    str = to_string(worker_id)
    IO.inspect("start makeAst #{str}")
    GenServer.start_link(__MODULE__, worker_id, name: via_tuple(worker_id))
  end

  @doc """
  Callback function called from within Genserver to initialize the process,
  The state consists of this tuple %{:name => worker_id, :value => 0}
  """
  @impl true
  def init(worker_id) do
    get_next(worker_id) # start a call to this process
    {:ok, %{:name => worker_id, :value => 0}}
  end

  @doc """
  Callback, responds to :nextid
  Get bestands_wijziging sourcecodes
  Saves it in a new  AbstractSyntaxTree object
  """
  @impl true
  def handle_cast({:nextid, [id|_]}, state) do
    IO.puts("next id")
    IO.puts(id)
    bestands_wijziging = get_bw_by_id(id) # data from db
    if bestands_wijziging != nil do
      IO.puts("bw opgehaald")
      IO.puts(bestands_wijziging.id)
      %AstCreator.AbstractSyntaxTree{
        bestandswijziging_id: bestands_wijziging.id,
        tekstvooraf_ast: getAstString(bestands_wijziging.tekstvooraf), # calls getAstString
        tekstachteraf_ast: getAstString(bestands_wijziging.tekstachteraf) # calls getAstString
      }
      |> saveAst # saves ast to db
    end

    next_id = id
    get_next(Map.get(state, :name)) # start next call
    state = %{:name => Map.get(state, :name), :value => next_id} # set new state,
    {:noreply, state}  # new state for next loop
  end

  @impl true
  def handle_cast({:noid, _}, state) do
    {:noreply, state}
  end

  @doc """
    Initiatesa a cast, help function
  """
  def cast(pid, {:nextid, id}) do
    GenServer.cast(pid, {:nextid, id})
  end

  def cast(pid, {:noid, _}) do
    GenServer.cast(pid, {:noid, nil})
  end

  @doc """
    Get data from db
  """
  def get_bw_by_id(id) do
    AstCreator.Repo.get(AstCreator.Bestandswijziging, id)
  end

  @doc """
    Create AST string
  """
  def getAstString(tekst) do
    case tekst do
      nil -> nil
      "[{:" <> _  -> "data file"
      _ ->
        case Code.string_to_quoted(tekst, unescape: false) do
          {:ok, ast} -> inspect(ast, limit: :infinity)
          {:error, {line, error, token}} -> "syntax error, " <> inspect({line, error, token})
        end
    end
  end

  @doc """
    Save to db
  """
  def saveAst(tree) do
    IO.puts("called save")
    AstCreator.Repo.insert(tree)
  end

  @doc """
    Get next id from queue
  """
  def get_next(worker_id) do
    x = AstCreator.GetFileChanges.next_filechange()
    if x != nil do
      cast(via_tuple(worker_id), {:nextid, x})
    else
      cast(via_tuple(worker_id), {:noid, x})
    end
  end

  @doc """
    this sets and gets the process id from AstCreator.ProcessRegistry
    based on the worker_id
  """
  def via_tuple(worker_id) do
    AstCreator.ProcessRegistry.via_tuple({__MODULE__, worker_id})
  end


end
