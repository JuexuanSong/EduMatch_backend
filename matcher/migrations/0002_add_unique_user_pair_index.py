from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE UNIQUE INDEX unique_match_users
            ON matcher_match (
                LEAST(user1_id, user2_id),
                GREATEST(user1_id, user2_id)
            );
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS unique_match_users;
            """
        )
    ]
