# Database Instructions

- first make sure that postgresql is running as a process in the background with "brew services start postgresql@18"
- then run "psql <dbname>" to get into your db
- if you want, you can run "psql -U postgres" to view all databases on your server
  - this gets you into the top level as a superuser
- to create a database, run "createdb <dbname>"
- when finished, stop the server by running "brew services stop postgresql"
