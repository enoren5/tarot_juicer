from django.apps import apps
from django.core.management import call_command
from django.db import connection, models
from django.db.migrations.loader import MigrationLoader
from django.test import TestCase, TransactionTestCase

from tarot_juicer.migration_ops import AddFieldIfMissing, RemoveFieldIfExists


def table_columns(table):
    with connection.cursor() as cursor:
        return {c.name for c in connection.introspection.get_table_description(cursor, table)}


class MigrationsFromScratchTests(TestCase):
    """The test database is built by running every migration from empty, so
    this class also fails during setup if any migration cannot run."""

    def test_models_have_no_unmigrated_changes(self):
        call_command("makemigrations", check=True, dry_run=True, verbosity=0)

    def test_migrated_columns_match_models(self):
        for label in ("generators", "landings"):
            for model in apps.get_app_config(label).get_models():
                expected = {f.column for f in model._meta.concrete_fields}
                self.assertEqual(table_columns(model._meta.db_table), expected, model._meta.label)


class TolerantOperationTests(TransactionTestCase):
    TABLE = "landings_howto"

    def setUp(self):
        self.state = MigrationLoader(connection).project_state()

    def apply(self, operation, from_state):
        to_state = from_state.clone()
        operation.state_forwards("landings", to_state)
        with connection.schema_editor() as editor:
            operation.database_forwards("landings", editor, from_state, to_state)
        return to_state

    def add_ghost(self, from_state):
        return self.apply(
            AddFieldIfMissing("howto", "ghost", models.BooleanField(default=True)), from_state
        )

    def test_add_skips_existing_column(self):
        self.apply(
            AddFieldIfMissing("howto", "is_published", models.BooleanField(default=True)),
            self.state,
        )
        self.assertIn("is_published", table_columns(self.TABLE))

    def test_add_then_remove_changes_the_table(self):
        with_ghost = self.add_ghost(self.state)
        self.assertIn("ghost", table_columns(self.TABLE))
        self.apply(RemoveFieldIfExists("howto", "ghost"), with_ghost)
        self.assertNotIn("ghost", table_columns(self.TABLE))

    def test_remove_skips_missing_column(self):
        state_only = self.state.clone()
        AddFieldIfMissing("howto", "ghost", models.BooleanField(default=True)).state_forwards(
            "landings", state_only
        )
        self.apply(RemoveFieldIfExists("howto", "ghost"), state_only)
        self.assertNotIn("ghost", table_columns(self.TABLE))
