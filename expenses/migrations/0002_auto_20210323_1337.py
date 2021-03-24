# Generated by Django 3.1.7 on 2021-03-23 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='expense',
            name='title',
            field=models.CharField(default='PSU', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
