# Generated by Django 5.0.4 on 2024-04-19 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_post_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
            ],
        ),
        migrations.RenameModel(
            old_name='LikePost',
            new_name='LikedPosts',
        ),
    ]