# Generated by Django 3.2.15 on 2022-09-05 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Города',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Deliveries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=70)),
                ('secondname', models.CharField(max_length=70)),
                ('phone', models.IntegerField()),
                ('status', models.CharField(max_length=70)),
                ('last_completed_order', models.DateTimeField(null=True)),
                ('card_number', models.CharField(max_length=70)),
                ('hours_worked', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=150, verbose_name='Адрес точки')),
                ('current_orders_count', models.IntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.cities', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Точки',
                'verbose_name_plural': 'Точки',
                'ordering': ['city'],
            },
        ),
    ]
