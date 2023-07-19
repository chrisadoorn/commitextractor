defmodule AstCreator.Bestandswijziging do
  use Ecto.Schema

  @schema_prefix "v11"

  schema "bestandswijziging" do
    field(:tekstvooraf, :string)
    field(:tekstachteraf, :string)
    field(:difftext, :string)
    field(:idcommit, :integer)
  end
end
