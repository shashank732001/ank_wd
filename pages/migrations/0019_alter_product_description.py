# Generated by Django 4.0.4 on 2022-05-02 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0018_alter_cartitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
