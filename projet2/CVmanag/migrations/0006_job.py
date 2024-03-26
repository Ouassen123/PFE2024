# Generated by Django 5.0.3 on 2024-03-13 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CVmanag', '0005_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('details', models.TextField()),
                ('image', models.ImageField(upload_to='job_images/')),
            ],
        ),
    ]
