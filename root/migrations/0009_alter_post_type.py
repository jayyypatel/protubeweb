# Generated by Django 4.0.6 on 2023-06-12 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0008_advertisement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('kids', 'kids'), ('teenager', 'teenager'), ('adult', 'adult'), ('general', 'general')], default='general', max_length=10),
        ),
    ]