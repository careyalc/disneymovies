import django_filters
from disneymovies.models import Movie, Genre


class DisneyMovieFilter(django_filters.FilterSet):
	movie_title = django_filters.CharFilter(
		field_name='movie_title',
		label='Movie Title',
		lookup_expr='icontains'
	)

	#filter by genre
	genre_name = django_filters.ModelChoiceFilter(
		field_name='genre__genre_name',
		# field_name='country_area__heritage_site_category__category_name',
		label='Genre',
		queryset = Genre.objects.all().order_by('genre_name'),
		lookup_expr='exact'
	)


	class Meta:
		model = Movie
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []