# Interacting with databases

## Takeaways

### Databases and SQL

- relational databases : primary and foreign keys
- `EXPLAIN` to see SQL execution plan
- indexes and views to speed up queries, [use the index](https://use-the-index-luke.com/fr)

### Client-server model

| Name            | Role                                                                                     | Example               |
|-----------------|------------------------------------------------------------------------------------------|-----------------------|
| Web client      | Handles input from user and sends requests to the web server                             | Browser, command line |
| Web server      | Receives requests from web client (server) and passes it to the database server (client) | Flask, php            |
| Database server | Receives requests from the web server and returns a response to the web server           | Postgresql            |
| Web server      | Receives response from the database server and passes it to the web client               |                       |
| Web client      | Displays the response from the web client for the user                                   |                       |

### ACID properties of transactions

* atomicity
* consistency
* isolation
* durability

### PostgreSQL

Usual command-line instructions

```bash
sudo -u <user> -i      # connect as user
createdb <db_name>     # create a database
dropdb <db_name>       # drop a database
createuser <user_name> # create a user
dropuser <user_name>   # drop a user
```

Within `psql` commands

```
\l          # list databases
\du         # list users
\c <dbname> # connect to database

\dt         # list tables of current database
\d <table>  # list details about table
```

## Code archive

### Course 4 - SQL exercices

Create `drivers` and `vehicles` tables

```sql
create table drivers (
  id serial primary key,
  first_name varchar,
  last_name varchar
);

create table vehicles (
  id serial primary key,
  make varchar,
  model varchar,
  driver_id integer references drivers(id)
);
```

Fill tables with some rows.


```sql
INSERT INTO drivers (first_name, last_name) VALUES
  ('Scott', 'Summers'),
  ('Logan', 'Unknown'),
  ('Jean', 'Grey') ;
  
INSERT INTO vehicles (make, model, driver_id) VALUES
  ('2010', 'Toyota', 1),
  ('2020', 'Renault', 2),
  ('2010', 'Citroën', 3) ;
  ('2020', 'Rorovelo', 3),
  ('1990', 'Toyota', 2);
```

Add email and phone columns, with a regex constraint on phone numbers.

```sql
ALTER TABLE drivers
ADD email VARCHAR(255),
ADD phone CHAR(10),
ADD CONSTRAINT phone_number CHECK (phone ~ '^[0-9]{10}$');

UPDATE drivers SET 
    email = "last_name" || '@xmen.com',
    phone = '0102030405'
WHERE first_name = 'Logan' ;
```

### Alert for yearly review within next month

Create a column with due date of car review for this year : day and month
of registration date but current year.

```sql
UPDATE vehicles
    SET next_review_date = to_date(
        DATE_PART('year', NOW()) || '-' ||
        DATE_PART('month', "date_of_registration") || '-' ||
        DATE_PART('day', "date_of_registration"),
        'YYYY-MM-DD'
     ) ;
```

Clean output of drivers and their vehicles

```sql
SELECT 
    first_name || ' ' || last_name AS person, 
    vehicles.id AS vehicle_id, 
    model,
    date_of_registration, next_review_date
FROM drivers, vehicles WHERE drivers.id = vehicles.driver_id 
ORDER BY date_of_registration DESC;
```

Query to get users with pending review within the current month.

```sql
SELECT first_name || ' ' || last_name AS person, phone, email, vehicles.id as vehicle_id
FROM drivers, vehicles
WHERE 
    drivers.id = vehicles.driver_id AND
    "next_review_date" <= NOW() + INTERVAL '1 month' AND
    "next_review_date" > NOW() ;
```

### Courses 17-20 Psycopg2

#### Init

Imports and create a set of rows for later insert.

```python
import psycopg2
import psycopg2.extras
from datetime import date
from random import randint
from pyux.time import Chronos

chrono = Chronos()

sample_rows = [
    (date(2020, 1, randint(1, 31)), str(randint(1, 5)))
    for i in range(int(1e4))
]
```

Connect to database and create tables (and enum).

```python
conn = psycopg2.connect("dbname={dbname}".format(dbname="gym"))

# DictCursor so that SELECT results are returned as a dictionary
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("DROP TABLE IF EXISTS workouts")
cursor.execute("DROP TYPE IF EXISTS intensity_rank")

cursor.execute("CREATE TYPE intensity_rank AS ENUM ('1', '2', '3', '4', '5')")
cursor.execute("""
    CREATE TABLE workouts(
        date DATE NOT NULL,
        intensity intensity_rank NOT NULL
    )
""")
chrono.lap('Tables created')
```

#### Insert

Insert values at once with appropriate string conversion. `cursor.mogrify`
returns an sql string with rightly converted types.

```python
insert_workouts_sql = "INSERT INTO workouts (date, intensity) VALUES {} ;"

insert_values = ", ".join(
    cursor.mogrify("(%s, %s)", row).decode("utf-8")
    for row in sample_rows
)
cursor.execute(insert_workouts_sql.format(insert_values))
chrono.lap('Execute string')
```

Insert values using a normal for loop (equivalent to `executemany`).

```python
for row in sample_rows:
    cursor.execute(insert_workouts_sql.format("(%s, %s)"), row)
chrono.lap('Execute loop')
```

Insert values with named variables using a dictionary.

```python
cursor.execute(
    insert_workouts_sql.format("(%(date)s, %(intens)s)"),
    {'date': date(2020, 1, 30), 'intens': '3'}
)
```

### Get

Fetch one value at a time.

```python
cursor.execute("SELECT * FROM workouts WHERE intensity = '3' LIMIT 10 ;")
one_record = cursor.fetchone()
```

Fetch values as a dictionary using cursor as a generator.

```python
cursor.execute("SELECT * FROM workouts ORDER BY date LIMIT 10 ;")
for workout in cursor:
    print("Workout from date {} was intensity {}".format(
        workout['date'], workout['intensity']
    ))
```

Terminate and print times to compare insert with strings and insert with a loop.

```python
conn.commit()
cursor.close()
conn.close()

chrono.compute_durations()
for key, value in chrono.durations.items():
    print("{} : {}".format(key, value))
```
