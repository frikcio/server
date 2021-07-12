# Generated by Django 3.2.4 on 2021-07-12 11:59
from django.contrib.auth.models import Group
from django.db import migrations


def create_groups(apps, schema_editor):
    # Create users groups for server
    Group.objects.bulk_create([
        Group(name='readers'),
        Group(name='writers'),
    ])    # Create readers and writers groups


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
