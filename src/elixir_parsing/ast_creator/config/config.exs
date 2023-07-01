import Config

config :ast_creator, ecto_repos: [AstCreator.Repo]

config :ast_creator, AstCreator.Repo,
  database: "multicore",
  username: "evert",
  password: "3Nosmoke3",
  hostname: "localhost"


