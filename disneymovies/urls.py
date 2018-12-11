from django.urls import path
from . import views 
from django_filters.views import FilterView

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movie_characters/', views.CharPageView.as_view(), name='movie_char'),
    path('movie_characters/<int:pk>/', views.CharDetailView.as_view(), name='char_detail'),
    path('movie_filter', views.MovieFilterView.as_view(), name='movie_filter'),
    path('movies/new/', views.MovieCreateView.as_view(), name='movie_new'),
	path('movies/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie_delete'),
	path('movies/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie_update')
]