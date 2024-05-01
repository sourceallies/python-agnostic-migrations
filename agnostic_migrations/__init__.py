import os
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass()
class AgnosticMigration:
    apply: Callable[[], None]
    revert: Callable[[], None] = lambda: print(
        "No revert method configured"
    )  # pragma: no cover


@dataclass()
class AgnosticMigratorStorage:
    def get_applied_migrations(self) -> List[str]:
        raise Exception("Not Implemented")  # pragma: no cover

    def save_migration(self, migration_name: str) -> None:
        raise Exception("Not Implemented")  # pragma: no cover


@dataclass()
class AgnosticMigratorInMemoryStorage(AgnosticMigratorStorage):
    _applied_migrations: List = field(default_factory=lambda: [])

    def get_applied_migrations(self):
        return self._applied_migrations

    def save_migration(self, migration_name: str):
        self._applied_migrations.append(migration_name)


@dataclass()
class AgnosticMigrationResults:
    successful_migrations: List = field(default_factory=lambda: [])
    reverted_migrations: List = field(default_factory=lambda: [])


@dataclass()
class AgnosticMigrator:
    migrations_path: str
    storage: AgnosticMigratorStorage

    def run_migrations(self) -> AgnosticMigrationResults:
        previously_applied_migrations = self.storage.get_applied_migrations()
        results = AgnosticMigrationResults()
        for file in sorted(os.listdir(self.migrations_path)):
            if file.endswith(".py"):
                if file in previously_applied_migrations:
                    print(f"Migration {file} has already been applied, skipping.")
                    continue
                f = open(os.path.join(self.migrations_path, file), "r")
                scriptLocals = {}
                exec(f.read(), scriptLocals)
                if "migration" in scriptLocals and isinstance(
                    scriptLocals["migration"], AgnosticMigration
                ):
                    migration: AgnosticMigration = scriptLocals["migration"]
                    try:
                        print(f"Executing migration {file}...")
                        migration.apply()
                        self.storage.save_migration(file)
                        results.successful_migrations.append(file)
                    except Exception as error:
                        print(
                            f"Migration {file} apply script failed with error {error}"
                        )
                        print(f"Executing revert script for migration {file}")
                        migration.revert()
                        results.reverted_migrations.append(file)
                        break
        return results
