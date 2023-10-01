defmodule AstCreator.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do # call back functin used by Application
    children = [
      AstCreator.Repo,
      AstCreator.System  # change System to System2 to create ASTs
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: AstCreator.Supervisor]
    IO.puts("starting application")
    Supervisor.start_link(children, opts)
  end
end
