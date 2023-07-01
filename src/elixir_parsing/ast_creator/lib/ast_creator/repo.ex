defmodule AstCreator.Repo do
  use Ecto.Repo,
    otp_app: :ast_creator,
    adapter: Ecto.Adapters.Postgres
end
