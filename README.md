
# Disney Movies
### by Alex Carey

## Purpose
My Disney Movies Django web app homepage will display a list view of available Disney Movies. If a user clicks on a movie, they are taken to a movie detail page where more information about a movie, such as its title, release date, director, genre, song, characters, and how much money it made, are displayed if that data is available in the disney_movies database. An image of the movie's cover is also displayed. 

From here, or from the Character list view in the navigation, if a user clicks on a character name, they can see who voiced that character. In some cases, a character will have more than once voice actor. 

A user can also filter their views of movies by searching for a date or title, or by selecting a director or genre from the drop down menu. If a movie fits the filter criteria, its title and release date are displayed. 

Finally, a user can add, edit, or delete a movie from the site (also updating the connected disney_movies database). This is done by clicking "new" on the home page, or "edit" or "delete" on a movie detail page. A user can also alter the database using the API that is part of this project. Additionally, this project utilizes social login in order to allow access to certain parts of the site.

Overall, my Disney Movies site will allow users to learn more about Disney Movies!

## Data Set
The data for this project was taken from a project found on data.world. The original files can be found [here](https://data.world/kgarrett/disney-character-success-00-16). I will not be using all of these files, but instead parts to create relationships between the actors, characters, movies, directors, etc. More details can be seen in the data model below. 

## Data Model
![Disney Model](/disneymovies/static/images/disney_model.png "data model")

## Package Dependencies 
Please ensure the following packages are installed in order to allow this site to run correctly:
![Pip List Image](/disneymovies/static/images/packages.png "packages needed")

## Final Notes!
In order to allow the images to show up on the detail pages, I had to manually name them the same number as their movie id, for example "2.jpg" Because of this, when the instructional team updates the database, I ask that a movie starting with "Zop" (or any word that would come after "Zootopia" in alphabetical order) be used as to allow the other pages to still load the correct movie images. 

I also want to note that while setting up my social login, I created another set of credentials specifically for this project, however it appears to still say "directing to heritagesites" from the Google social login page. I've tested this and it will still direct you back to my disneymovies site!

# Thanks! 
 