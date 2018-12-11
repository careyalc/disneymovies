from django.urls import path
from . import views 
# from django_filters.views import FilterView

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movie_characters/', views.CharPageView.as_view(), name='movie_char'),
    path('movie_characters/<int:pk>/', views.CharDetailView.as_view(), name='char_detail'),
]