# FastApi_Chat_GPT
### PostgreSQL Setup:
Install PostgreSQL via Homebrew (Mac):
1. `brew install postgresql`
2. `brew services start postgresql`
3. `psql postgres`

Create a User and Database

-- Create a user

`CREATE USER user WITH PASSWORD 'password';`

-- Create a database

`CREATE DATABASE db;`

-- Grant all privileges to the user for the database

`GRANT ALL PRIVILEGES ON DATABASE chat_db TO myuser;`

-- Grant superuser privileges to the user (optional)

`ALTER USER myuser WITH SUPERUSER;`


### Налаштування змінних середовища
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DATABASE_URL=
```

### Running the containers via Makefile

`make up`

### Stopping the containers via Makefile

`make down`
