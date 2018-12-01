from django.db import models
from django.urls import reverse

class DisneyMovie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_title = models.CharField(unique=True, max_length=100)
    # director = models.CharField(max_length=45)
    dir_id = models.IntegerField(blank=True)
    release_date = models.CharField(max_length=45)
    # genre = models.CharField(max_length=45, null=True)
    genre_id = models.IntegerField(blank=True)
    song = models.CharField(max_length=100, null=True)
    total_gross = models.IntegerField(blank=True, null=True)
    inflation_gross = models.IntegerField(blank=True, null=True)
    # heritage_site_category = models.ForeignKey('HeritageSiteCategory', on_delete=models.PROTECT)

    # Intermediate model (country_area -> heritage_site_jurisdiction <- heritage_site)
    # country_area = models.ManyToManyField(CountryArea, through='HeritageSiteJurisdiction')

    class Meta:
        managed = False
        db_table = 'movie'
        ordering = ['movie_title']
        verbose_name = 'Disney Movie'
        verbose_name_plural = 'Disney Movies'

    def __str__(self):
        return self.movie_title

    def get_absolute_url(self):
        # return reverse('site_detail', args=[str(self.id)])
        return reverse('movie_detail', kwargs={'pk': self.pk})
