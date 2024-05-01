from agnostic_migrations import AgnosticMigration


def apply():
    print("Running apply")


def revert():
    print("Running revert")


migration = AgnosticMigration(apply, revert)
