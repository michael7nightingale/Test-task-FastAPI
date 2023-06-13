# Web-application for employees.

Application is written using FastAPI framework (really it is a test task). I tried many different versions of architecture,
but this one seems to be the best. I really hope you like it, I just tried to user everything I know on 
this kind of project and user some new tools (poetry, pytest, docker). It is not over-engineering for this task, it's
comfort app to change and add, to broad it. Waiting for your issues and PR's.

## Task (literally)
Build REST-service for watching current salary and date of the next promotion.
Every employee is able to watch its own data because data is very important and critical.
For the security providing, you should realize method for getting time-expiring token
by employee's login and password. Data on employee's request is to be shown only if token validation is 
successful.

### Requirements for solution:
 Must-have:
- code is published on the public `GitLab` repository;
- the project-constructing instruction is provided;
- `FastAPI` realization.

Non must-have:
- `poetry` pacakge manager;
- `pytest` tests;
- `Docker` containers.






