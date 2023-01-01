# Generated by Django 4.1.1 on 2022-11-12 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("NearBeach", "0022_alter_campus_campus_address1_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quote",
            name="change_user",
        ),
        migrations.RemoveField(
            model_name="quote",
            name="creation_user",
        ),
        migrations.RemoveField(
            model_name="quote",
            name="customer",
        ),
        migrations.RemoveField(
            model_name="quote",
            name="opportunity",
        ),
        migrations.RemoveField(
            model_name="quote",
            name="organisation",
        ),
        migrations.RemoveField(
            model_name="quote",
            name="project",
        ),
        migrations.RemoveField(
            model_name="quote",
            name="quote_billing_address",
        ),
        migrations.RemoveField(
            model_name="quote",
            name="quote_stage",
        ),
        migrations.RemoveField(
            model_name="quote",
            name="task",
        ),
        migrations.RemoveField(
            model_name="whiteboard",
            name="change_user",
        ),
        migrations.RemoveField(
            model_name="document",
            name="whiteboard",
        ),
        migrations.RemoveField(
            model_name="document_permission",
            name="whiteboard",
        ),
        migrations.RemoveField(
            model_name="email_contact",
            name="quotes",
        ),
        migrations.RemoveField(
            model_name="object_assignment",
            name="quote",
        ),
        migrations.RemoveField(
            model_name="object_assignment",
            name="whiteboard",
        ),
        migrations.RemoveField(
            model_name="object_note",
            name="quote",
        ),
        migrations.DeleteModel(
            name="list_of_quote_stage",
        ),
        migrations.DeleteModel(
            name="quote",
        ),
        migrations.DeleteModel(
            name="whiteboard",
        ),
    ]