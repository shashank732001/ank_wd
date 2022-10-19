# Generated by Django 4.0.4 on 2022-05-02 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.product'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Delivered', 'Delivered')], default='Pending', max_length=200, null=True),
        ),
    ]
