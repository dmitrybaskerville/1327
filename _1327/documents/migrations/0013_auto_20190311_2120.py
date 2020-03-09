# Generated by Django 2.0.13 on 2019-03-11 20:20

from django.db import migrations, models


def copy_german_titles(apps, _schema_editor):
    Document = apps.get_model("documents", "Document")
    for document in Document.objects.all():
        if not document.title_en:
            document.title_en = document.title_de
            document.save()


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0012_auto_20181228_1942'),
    ]

    operations = [
        migrations.RunPython(copy_german_titles, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='document',
            name='title_de',
            field=models.CharField(max_length=255, verbose_name='title (german)'),
        ),
        migrations.AlterField(
            model_name='document',
            name='title_en',
            field=models.CharField(max_length=255, verbose_name='title (english)'),
        ),
    ]
