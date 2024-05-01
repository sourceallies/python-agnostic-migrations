# python-agnostic-migrations

Extremely simple migration tool for python projects that is agnostic to what it is migrating.

## Usage

Create an instance of `AgnosticMigrator` and pass in 2 things:

1. An absolute path to a folder containing migration files
2. A storage mechanism to keep track of what migrations have been run. It will need to be an implementation of the `AgnosticMigratorStorage" class

We provide a sample implementation of `AgnosticMigratorInMemoryStorage` for running tests or trying out the library, but it is recommended to use a storage service of some kind, like s3, dynamodb, file storage, or a database.

### Example

```python
import os
from agnostic_migrations import AgnosticMigrator, AgnosticMigratorInMemoryStorage

migrations_path = os.path.dirname(os.path.abspath(__file__)) + "/migrations"

def execute(): 
  migrator = AgnosticMigrator(
      migrations_path,
      AgnosticMigratorInMemoryStorage() #  or your storage implementation here
  )
  migrator.run_migrations()
```

## Migrations

The migration files have no specific naming convention.  The process will simply consider every file ending in `.py` as a migration file, and process them in alphabetical order.  Because of this, it is recommended to prefix with equal digit number, like so:

- 001-initial-migration.py
- 002-update-schema.py
- 003-add-user.py

### Example Migration File

Migration files must create a `migration` variable that is an instance of `AgnosticMigration` to be valid.

```python
from agnostic_migrations import AgnosticMigration

def apply():
    print("Migrating application state.")
    # Execute custom code here to interface with tool you wish to run migration against


def revert():
    print("An error occurred during application. Safely roll back changes here.")
    # Execute custom code here to interface with tool you wish to run revert against in the case of a failed apply

migration = AgnosticMigration(apply, revert)
```

## WHY?

Having an agnostic migration tool is very helpful for 2 cases:

1. The tool you are wanting to manage is not a traditional relational database, and you want to be able to use a liquibase/flyway style migration to manage its state reliably and at scale.
2. You want to be able to manage the migrations or state of multiple dependencies with the same tooling.
3. You want to be able to leverage existing code in your codebase to interact with the tool and create the migrations.  This can be something like an sdk you are familiar with, or custom code you have already written for your application.

## Inspiration

This library was created as a lightweight python implementation of a pattern similar to [Umzug](https://github.com/sequelize/umzug), which is a similar tool written for typescript.