# Generated by Django 2.1.7 on 2019-03-22 03:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('airline3app', '0006_auto_20190317_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketHolders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PNR', models.PositiveIntegerField()),
                ('passenger_firstname', models.CharField(max_length=100)),
                ('passenger_lastname', models.CharField(max_length=100)),
                ('passenger_age', models.PositiveIntegerField()),
                ('passenger_gender', models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE'), ('other', 'OTHER')], default='female', max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PNR', models.PositiveIntegerField(unique=True)),
                ('username', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='passengers',
            name='passenger_age',
            field=models.PositiveIntegerField(),
        ),
    ]
