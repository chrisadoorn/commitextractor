# Author identifier

This module's task is to try to get the GitHub author_id of a committer

# Start proces

The module main.py which contains a _ _ main _ _ method.  Run this method to start execution.

# Settings

This module makes contact with the GitHub API.  To do this you need to have a GitHub account and a personal access token.  You can create a personal access token by going to your GitHub account settings and then to the developer settings.  You can find more information about this [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

Save your GitHub personal access token in the commitextractor.ini file like this:
```
[github]
personal_access_token = your personal access token
```

To module will read the content of verwerk_project table in the database. 
It will process all projects from this table where the value of processtap is 'extractie'.
You may have to set this value manually in the database if you want to run this module again.

```sql
--update query:
update verwerk_project set processtap = 'extractie', resultaat = 'verwerkt', start_verwerking = null, einde_verwerking = null;
```

For each project in the `verwerk_project` table the `commitinfo` belonging to that project will be retrieved from the database base.

For each commit from the `commitinfo` table first a check is done to see if the author_id is already known.  
If so, the next step is skipped and the known author_id will be assigned to teh commit.  
If not, a request is made to the GitHub API to get the author_id based on the commit hasvalue.
If the request is successful, the author_id will be assigned to the commit otherwise the author_id will be generated by the module.

The module does not run in parallel.  It processes one `commitinfo` at a time. 
Reason for this is that the GitHub API has a limit on the number of requests per hour, more requests will exceed this limit and is thus pointless. 
