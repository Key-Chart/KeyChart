# Generated by Django 5.2 on 2025-05-28 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atletas', '0004_alter_atleta_email_alter_atleta_telefone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atleta',
            name='altura',
            field=models.IntegerField(blank=True),
        ),
    ]
