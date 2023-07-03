defmodule AstCreator do
  import Ecto.Query, only: [from: 2]

  def get_by_id(id) do
    AstCreator.Repo.get(AstCreator.Bestandswijziging, id)
  end

  def getAstTekstVooraf(id) do
    z = get_by_id(id)
    {_ , ast} = Code.string_to_quoted(z.tekstvooraf,[])
  end

  def getAstTekstAchteraf(id) do
    z = get_by_id(id)
    {_ , ast} = Code.string_to_quoted(z.tekstachteraf,[])
  end

  def saveAst(tree) do
    AstCreator.Repo.insert(tree)
  end

  def getAndSave(id) do
    getAST(id) |>  saveAst
  end

  def getAST(id) do
    z = get_by_id(id)
    %AstCreator.AbstractSyntaxTree{
      bestandswijziging_id: id,
      tekstvooraf: z.tekstvooraf,
      tekstachteraf: z.tekstachteraf,
      difftext: z.difftext,
      tekstvooraf_ast: getAstString(z.tekstvooraf),
      tekstachteraf_ast: getAstString(z.tekstachteraf)
      }
  end

  defp getAstString(tekst) do
    case tekst do
      nil -> nil
      _ ->
        case Code.string_to_quoted(tekst, []) do
          {:ok ,ast} -> (inspect ast, limit: :infinity)
          {:error, _} -> "syntax error"
        end
    end
  end

  def getAllBestandswijzigingIds() do
    q = from u in AstCreator.Bestandswijziging, select: u.id
    list = AstCreator.Repo.all(q)
    counter = 0
    a = Enum.reduce(list, [], fn(x, acc) ->
      t = acc ++ [x]
      if length(t) == 50000 do
        IO.puts "next 50000"
        IO.inspect x
        spawn(fn ->
          IO.inspect(self())
          useCC(t)
        end)
        IO.puts "reset acc"
        []
        else
        t
      end

    end)

    IO.puts "last batch"
    IO.inspect length(a)
    spawn(fn ->
      IO.inspect(self())
      useCC(a)
    end)
  end

  def useCC([x | y]) do
      case {x, y} do
        {x,[]} -> getAndSave(x)
        {x, y} -> getAndSave(x)
                  useCC(y)
      end
  end



end
