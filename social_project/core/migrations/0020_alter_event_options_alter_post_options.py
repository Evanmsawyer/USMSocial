# Generated by Django 5.0.3 on 2024-04-22 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_event'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'permissions': [('can_delete_events', 'Can delete events')]},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': [('can_delete_posts', 'Can delete posts')]},
        ),
    ]
