# Generated by Django 5.0.1 on 2024-01-17 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_test', '0010_alter_user_idstatus_delete_usertype_delete_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achivement',
            name='forKarl',
        ),
        migrations.AddField(
            model_name='achivement',
            name='boscoFriend',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='digGrave',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='fallen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='faster',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='friend',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='molyBatle',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='notPassed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='party',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='perfectShoot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='unpredictable',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='waveComming',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='achivement',
            name='winner',
            field=models.IntegerField(default=0),
        ),
    ]