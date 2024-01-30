# Generated by Django 4.0.8 on 2024-01-30 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_activitylog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsandevents',
            name='posted_as',
            field=models.CharField(choices=[('News', 'Yangilik'), ('Event', 'Voqelik')], max_length=10),
        ),
        migrations.AlterField(
            model_name='semester',
            name='semester',
            field=models.CharField(blank=True, choices=[('First', 'Birinchi'), ('Second', 'Ikkinchi'), ('Third', 'Uchinchi')], max_length=10),
        ),
    ]