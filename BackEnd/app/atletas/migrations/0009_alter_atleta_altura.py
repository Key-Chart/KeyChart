# Generated by Django 5.2 on 2025-05-29 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atletas', '0008_alter_atleta_altura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atleta',
            name='altura',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
