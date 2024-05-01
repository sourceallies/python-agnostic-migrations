import os

from agnostic_migrations import AgnosticMigrator, AgnosticMigratorInMemoryStorage

base_path = os.path.dirname(os.path.abspath(__file__)) + "/resources"


def test_agnostic_migrations():
    migrator = AgnosticMigrator(
        f"{base_path}/basic-migrations", AgnosticMigratorInMemoryStorage()
    )
    migrations = migrator.run_migrations()
    assert migrations.successful_migrations == ["1.py", "2.py"]
    assert migrations.reverted_migrations == []


def test_failing_migration_stops_execution():
    migrator = AgnosticMigrator(
        f"{base_path}/error-migrations", AgnosticMigratorInMemoryStorage()
    )
    migrations = migrator.run_migrations()
    assert migrations.successful_migrations == ["1.py"]
    assert migrations.reverted_migrations == ["2.py"]


def test_invalid_migration_does_not_run():
    migrator = AgnosticMigrator(
        f"{base_path}/invalid-migrations", AgnosticMigratorInMemoryStorage()
    )
    migrations = migrator.run_migrations()
    assert migrations.successful_migrations == ["1.py"]
    assert migrations.reverted_migrations == []


def test_migration_does_not_apply_again():
    migrator = AgnosticMigrator(
        f"{base_path}/basic-migrations", AgnosticMigratorInMemoryStorage()
    )
    migrator.run_migrations()
    migrations = migrator.run_migrations()
    assert migrations.successful_migrations == []
    assert migrations.reverted_migrations == []


def test_migration_does_not_apply_again_with_existing_memory():
    migrator = AgnosticMigrator(
        f"{base_path}/basic-migrations", AgnosticMigratorInMemoryStorage(["1.py"])
    )
    migrations = migrator.run_migrations()
    assert migrations.successful_migrations == ["2.py"]
    assert migrations.reverted_migrations == []
