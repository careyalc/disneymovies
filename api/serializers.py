from disneymovies.models import Movie, Director, Genre, Actor, MovieCharacter, Credit
from rest_framework import response, serializers, status


class DirectorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Director
		fields = ('director_id', 'director_name')


class GenreSerializer(serializers.ModelSerializer):

	class Meta:
		model = Genre
		fields = ('genre_id', 'genre_name')


class ActorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Actor
		fields = ('actor_id', 'actor_name')


# class LocationSerializer(serializers.ModelSerializer):
# 	planet = PlanetSerializer(many=False, read_only=True)
# 	region = RegionSerializer(many=False, read_only=True)
# 	sub_region = SubRegionSerializer(many=False, read_only=True)
# 	intermediate_region = IntermediateRegionSerializer(many=False, read_only=True)

# 	class Meta:
# 		model = Location
# 		fields = ('location_id', 'planet', 'region', 'sub_region', 'intermediate_region')



# class CountryAreaSerializer(serializers.ModelSerializer):
# 	dev_status = DevStatusSerializer(many=False, read_only=True)
# 	location = LocationSerializer(many=False, read_only=True)

# 	class Meta:
# 		model = CountryArea
# 		fields = (
# 			'country_area_id',
# 			'country_area_name',
# 			'm49_code',
# 			'iso_alpha3_code',
# 			'dev_status',
# 			'location')


# class HeritageSiteCategorySerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = HeritageSiteCategory
# 		fields = ('category_id', 'category_name')


class CreditSerializer(serializers.ModelSerializer):
	movie_id = serializers.ReadOnlyField(source='movie.movie_id')
	movie_character_id = serializers.ReadOnlyField(source='movie_character.movie_character_id')
	actor_id = serializers.ReadOnlyField(source='actor.actor_id')

	class Meta:
		model = Credit
		fields = ('movie_id', 'movie_character_id', 'actor_id') #double check that this should not be movie_title and movie_character_name

class CreditUserSerializer(serializers.Serializer):
	movie_character_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=MovieCharacter.objects.all(), source='movie_character')
	actor_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Actor.objects.all(), source="actor")


class MovieSerializer(serializers.ModelSerializer):
	movie_title = serializers.CharField(
		allow_null=False,
		max_length=100
	)
	director = DirectorSerializer(
		many=False,
		read_only=True
	)
	director_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=Director.objects.all(),
		source='director'
	) #is this primary key related thing necessary? or would I just need this for movie_characters because that is what is in my model?
	release_date = serializers.CharField(
		allow_blank=False
	)
	genre = GenreSerializer(
		many=False,
		read_only=True
	)
	genre_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=Genre.objects.all(),
		source='genre'
	) #not sure if this is needed either 
	song = serializers.CharField(
		allow_null=True
	)
	total_gross = serializers.IntegerField(
		allow_null=True
	)
	inflation_gross = serializers.IntegerField(
		allow_null=True
	)
	credit = CreditSerializer(
		source='credit_set', # Note use of _set
		many=True,
		read_only=True
	) #should this be called movie_character like in model?
	# credit_ids = serializers.PrimaryKeyRelatedField(
	# 	many=True,
	# 	write_only=True,
	# 	queryset=MovieCharacter.objects.all(),
	# 	source='credit'
	# ) 
	credit_ids = CreditUserSerializer(
		many=True,
		write_only=True,
		source='credit'
	) 

	class Meta:
		model = Movie
		fields = (
			'movie_id',
			'movie_title',
			'director',
			'director_id', #not sure if needed
			'release_date',
			'genre',
			'genre_id', #not sure if needed
			'song',
			'total_gross',
			'inflation_gross',
			'credit',
			'credit_ids'
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""
		#POST
		# print(validated_data)

		movie_characters = validated_data.pop('credit')
		newmovie = Movie.objects.create(**validated_data) 
		# movie_id = movie.movie_id


		if movie_characters is not None:
			for movie_character in movie_characters:
				Credit.objects.create(
					movie_character=movie_character["movie_character"],
					actor=movie_character["actor"],
					movie=newmovie
					# movie_id=movie_character[2]["movie_id"]
					# movie_id=movie.movie_id,
					# movie_character_id=movie_character.movie_character_id
				)
		return newmovie

	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id') #PUT
		movie_id = instance.movie_id
		new_movie_characters = validated_data.pop('credit')

		instance.movie_title = validated_data.get(
			'movie_title',
			instance.movie_title
		)
		instance.director = validated_data.get(
			'director',
			instance.director
		)         #or would it be the id instead like in the heritage sites? #added id, but should take out if not needed above...
		instance.release_date = validated_data.get(
			'release_date',
			instance.release_date
		)
		instance.genre = validated_data.get(
			'genre',
			instance.genre
		)              #again, should it be id instead? #same as above...
		instance.song = validated_data.get(
			'song',
			instance.song
		)
		instance.total_gross = validated_data.get(
			'total_gross',
			instance.total_gross
		)
		instance.inflation_gross = validated_data.get(
			'inflation_gross',
			instance.inflation_gross
		)
		instance.save()

		# If any existing movie characters (?) are not in updated list, delete them...
		new_ids = []
		old_ids = Credit.objects \
			.values_list('movie_character_id', flat=True) \
			.filter(movie_id__exact=movie_id)

		# Insert may not be required (Just return instance) ... so, is below not needed? should I delete?

		# Insert new unmatched
		for movie_character in new_movie_characters:
			new_id = movie_character.movie_character_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				Credit.objects \
					.create(movie_id=movie_id, movie_character_id=new_id)

		# Delete old unmatched country entries - in my case, movie characters? 
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				Credit.objects \
					.filter(movie_id=movie_id, movie_character_id=old_id) \
					.delete()

		return instance