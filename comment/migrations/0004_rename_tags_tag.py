# Generated by Django 5.1.2 on 2024-11-15 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_rename_tag_tags_caption_alter_post_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
    ]