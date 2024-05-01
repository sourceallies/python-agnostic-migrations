from agnostic_migrations import AgnosticMigration


def apply():
    raise Exception("Bad thing happened")


def revert():
    print("Running revert")


migration = AgnosticMigration(apply, revert)
