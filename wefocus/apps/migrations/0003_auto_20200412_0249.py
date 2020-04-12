# Generated by Django 3.0.5 on 2020-04-12 02:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_partymember_pomodorotimer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partymember',
            options={'verbose_name_plural': 'party_members'},
        ),
        migrations.AddField(
            model_name='partymember',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='partymember',
            name='joined_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partymember',
            name='left_at',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='partymember',
            name='party_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partymember',
            name='role',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partymember',
            name='user_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='partymember',
            unique_together={('active', 'party_id', 'user_id')},
        ),
    ]
