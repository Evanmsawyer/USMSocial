# Generated by Django 5.0.4 on 2024-04-20 20:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='core.profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
