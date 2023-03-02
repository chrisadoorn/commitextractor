set schema 'test';

--DROP TABLE IF EXISTS gh_search_selection;

CREATE TABLE IF NOT EXISTS gh_search_selection
(
    id SERIAL,
    name VARCHAR,
    is_fork BOOLEAN,
    commits INTEGER,
    branches INTEGER,
    default_branch VARCHAR,
    releases INTEGER,
    contributors INTEGER,
    license VARCHAR,
    watchers INTEGER,
    stargazers INTEGER,
    forks INTEGER,
    size BIGINT,
    created_at TIMESTAMP,
    pushed_at TIMESTAMP,
    updated_at TIMESTAMP,
    homepage VARCHAR,
    main_language VARCHAR,
    total_issues INTEGER,
    open_issues INTEGER,
    total_pull_requests INTEGER,
    open_pull_requests INTEGER,
    last_commit TIMESTAMP,
    last_commit_sha VARCHAR,
    has_wiki BOOLEAN,
    is_archived BOOLEAN,
    import_date DATE NOT NULL DEFAULT CURRENT_DATE,
    sub_study VARCHAR,
    CONSTRAINT pk_gh_search_selection PRIMARY KEY (id)
)