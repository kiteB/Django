# Generated by Django 3.1.4 on 2021-01-02 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('third', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.IntegerField()),
                ('comment', models.CharField(max_length=500)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='third.restaurant')),
            ],
        ),
    ]