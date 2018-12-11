from django.db import models
from django.urls import reverse

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_title = models.CharField(unique=True, max_length=100)
    director = models.ForeignKey('Director', on_delete=models.PROTECT)
    # dir_id = models.IntegerField(blank=True)
    release_date = models.CharField(max_length=45)
    genre =  models.ForeignKey('Genre', on_delete=models.PROTECT)
    # genre_id = models.IntegerField(blank=True)
    song = models.CharField(max_length=100, null=True)
    total_gross = models.IntegerField(blank=True, null=True)
    inflation_gross = models.IntegerField(blank=True, null=True)
    # heritage_site_category = models.ForeignKey('HeritageSiteCategory', on_delete=models.PROTECT)
    # disney_movie_char = models.ForeignKey('DisneyChar', on_delete=models.PROTECT)

    # Intermediate model (country_area -> heritage_site_jurisdiction <- heritage_site)
    # country_area = models.ManyToManyField(CountryArea, through='HeritageSiteJurisdiction')
    # characters = models many to many through credit table
    movie_characters = models.ManyToManyField('MovieCharacter', through='Credit') 

    class Meta:
        managed = False
        db_table = 'movie'
        ordering = ['movie_title']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.movie_title

    def get_absolute_url(self):
        # return reverse('site_detail', args=[str(self.id)])
        return reverse('movie_detail', kwargs={'pk': self.pk})


class Director(models.Model):
    director_id = models.AutoField(primary_key=True)
    director_name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'director'
        ordering = ['director_name']
        verbose_name = 'Disney Director'
        verbose_name_plural = 'Disney Directors'

    def __str__(self):
        return self.director_name


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'genre'
        ordering = ['genre_name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.genre_name



class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    actor_name = models.CharField(unique=True, max_length=50)
    # movie_character = models.ManyToManyField('MovieCharacter', through='Credit')

    class Meta:
        managed = False
        db_table = 'actor'
        ordering = ['actor_name']
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'

    def __str__(self):
        return self.actor_name



class MovieCharacter(models.Model):
    movie_character_id = models.AutoField(primary_key=True)
    movie_character_name = models.CharField(unique=True, max_length=150)
    actor = models.ManyToManyField('Actor', through='Credit')
    # credit = models.ForeignKey('Credit', on_delete=models.CASCADE)
    # characters = models many to many through credit table

    class Meta:
        managed = False
        db_table = 'movie_character'
        ordering = ['movie_character_name']
        verbose_name = 'Disney Movie Character'
        verbose_name_plural = 'Disney Movie Characters'

    def __str__(self):
        return self.movie_character_name

    def get_absolute_url(self):
        # return reverse('site_detail', args=[str(self.id)])
        return reverse('movie_character_name', kwargs={'pk': self.pk})


class Credit(models.Model):
    credit_id = models.AutoField(primary_key=True)
    movie_character = models.ForeignKey('MovieCharacter', on_delete=models.CASCADE)
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'credit'
        ordering = ['movie']
        verbose_name = 'Credit'
        verbose_name_plural = 'Credits'





