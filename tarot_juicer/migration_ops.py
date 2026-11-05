"""Migration operations that tolerate databases whose schema has drifted.

Some databases for this project already have, or have already lost, a column
that a migration would add or remove. These operations check the real table
first, on any database backend, instead of using Postgres-only
`ADD COLUMN IF NOT EXISTS` / `DROP COLUMN IF EXISTS` SQL.
"""
from django.db import migrations


def _has_column(schema_editor, table, column):
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        description = connection.introspection.get_table_description(cursor, table)
    return column in {col.name for col in description}


class AddFieldIfMissing(migrations.AddField):
    """AddField that leaves the database alone if the column already exists.

    Pass drop_on_reverse=False when an earlier migration normally created the
    column, so that reversing this one does not remove it.
    """

    def __init__(self, *args, drop_on_reverse=True, **kwargs):
        self.drop_on_reverse = drop_on_reverse
        super().__init__(*args, **kwargs)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(app_label, self.model_name)
        column = model._meta.get_field(self.name).column
        if not _has_column(schema_editor, model._meta.db_table, column):
            super().database_forwards(app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        model = from_state.apps.get_model(app_label, self.model_name)
        column = model._meta.get_field(self.name).column
        if self.drop_on_reverse and _has_column(schema_editor, model._meta.db_table, column):
            super().database_backwards(app_label, schema_editor, from_state, to_state)


class RemoveFieldIfExists(migrations.RemoveField):
    """RemoveField that does nothing if the column is already gone.

    Reversing it restores the field in migration state only, not the column.
    """

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = from_state.apps.get_model(app_label, self.model_name)
        column = model._meta.get_field(self.name).column
        if _has_column(schema_editor, model._meta.db_table, column):
            super().database_forwards(app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass
