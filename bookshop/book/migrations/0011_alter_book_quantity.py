# Generated by Django 4.2.4 on 2023-10-03 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_book_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]