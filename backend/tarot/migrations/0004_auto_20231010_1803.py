# Generated by Django 3.2 on 2023-10-10 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tarot', '0003_auto_20231008_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='is_subscribed',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='price',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='role',
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='tarot.user'),
        ),
    ]