# Generated by Django 5.2 on 2025-05-29 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atletas', '0007_alter_atleta_altura_alter_atleta_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atleta',
            name='altura',
            field=models.IntegerField(blank=True, max_length=15),
        ),
    ]
