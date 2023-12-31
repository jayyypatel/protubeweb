# Generated by Django 4.0.6 on 2023-06-10 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0007_friendrequest_mode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('duration', models.IntegerField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
            ],
        ),
    ]
