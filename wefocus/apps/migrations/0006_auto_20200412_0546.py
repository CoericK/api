# Generated by Django 3.0.5 on 2020-04-12 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_auto_20200412_0522'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='member_count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterIndexTogether(
            name='party',
            index_together={('active', 'member_count', 'max_member_count'), ('active', 'host_user_id')},
        ),
    ]
