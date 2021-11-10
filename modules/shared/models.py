import peewee


# Connect to a Postgres database.
database = peewee.PostgresqlDatabase(
    "database",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432,
)


class Base(peewee.Model):
    class Meta:
        database = database
