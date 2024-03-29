defmodule AstCreator.AbstractSyntaxTree do
  use Ecto.Schema

  @schema_prefix "v11"

  schema "abstract_syntax_trees" do
    field(:bestandswijziging_id, :integer)
    field(:tekstvooraf_tokens, :string)
    field(:tekstachteraf_tokens, :string)
    field(:difftext, :string)
    field(:tekstvooraf_ast, :string)
    field(:tekstachteraf_ast, :string)
  end
end
