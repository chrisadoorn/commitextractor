defmodule AstCreator do

  def get_by_id(id) do
    AstCreator.Repo.get(AstCreator.Bestandswijziging, id)
  end

  def getAstTekstVooraf(id) do
    z = get_by_id(id)
    Code.string_to_quoted(z.tekstachteraf,[])
  end

  def getAstTekstAchteraf(id) do
    z = get_by_id(id)
    Code.string_to_quoted(z.tekstchteraf,[])
  end
end
