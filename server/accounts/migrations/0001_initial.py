# Generated by Django 3.2.4 on 2021-07-02 07:05

import django.contrib.auth.validators
from django.contrib.auth.models import UserManager, Group, Permission
from django.db import migrations, models
import django.utils.timezone

readers_group, created = Group.objects.get_or_create(name='readers')
read_board = Permission.objects.get(codename='view_board')
read_topic = Permission.objects.get(codename='view_topic')
read_post = Permission.objects.get(codename='view_post')
readers_group.permissions.add(read_board, read_topic, read_post)

writers_group, created = Group.objects.get_or_create(name='writers')
board_list = Permission.objects.filter(codename__contains='board').exclude(codename__contains='delete')
topic_list = Permission.objects.filter(codename__contains='topic').exclude(codename__contains='delete')
post_list = Permission.objects.filter(codename__contains='post').exclude(codename__contains='delete')
writers_permissions = board_list | topic_list | post_list
writers_group.permissions.set(writers_permissions)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('confirm_email', models.BooleanField(default=False)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', UserManager()),
            ],
        ),
    ]
