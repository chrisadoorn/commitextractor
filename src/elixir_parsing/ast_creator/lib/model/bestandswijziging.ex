defmodule AstCreator.Bestandswijziging do
  use Ecto.Schema

  @schema_prefix "v10"

  schema "bestandswijziging" do
    field :tekstvooraf, :string
    field :tekstachteraf, :string
    field :idcommit, :integer
  end
end