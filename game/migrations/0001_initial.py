# Generated by Django 3.2.9 on 2022-01-24 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('total_rating', models.FloatField(blank=True, null=True)),
                ('summary', models.TextField(blank=True)),
                ('first_release_date', models.DateField(blank=True, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('rating_count', models.IntegerField(blank=True, null=True)),
                ('aggregated_rating', models.FloatField(blank=True, null=True)),
                ('aggregated_rating_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-first_release_date'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('abbreviation', models.CharField(blank=True, max_length=40)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserFavouriteGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_games', to='game.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_games', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_related_name': 'favourite_games',
            },
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('image_id', models.URLField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='genres',
            field=models.ManyToManyField(blank=True, to='game.Genre'),
        ),
        migrations.AddField(
            model_name='game',
            name='platforms',
            field=models.ManyToManyField(blank=True, to='game.Platform'),
        ),
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('image_id', models.URLField()),
                ('game', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
            ],
        ),
    ]
