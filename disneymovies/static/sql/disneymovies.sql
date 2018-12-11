--
-- Create database
--

-- CREATE DATABASE IF NOT EXISTS disney_movies;
-- USE disney_movies;

--
-- Drop tables
-- turn off FK checks temporarily to eliminate drop order issues
--

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS motive, movie_character, actor, genre, director, temp_movie, movie, credit, temp_chars;
SET FOREIGN_KEY_CHECKS=1;

--
-- MOTIVE TABLE
--

CREATE TABLE IF NOT EXISTS motive
  (
    motive_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    motive_name VARCHAR(10) NOT NULL UNIQUE,
    PRIMARY KEY (motive_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO motive (motive_name) VALUES
  ('Hero'), ('Villian');


--
-- CHARACTER TABLE
--

CREATE TABLE IF NOT EXISTS movie_character
  (
    movie_character_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    movie_character_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (movie_character_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/alexandracarey/Documents/Third_Semester/664/Final_Project/disney/output/disney_character.csv'
INTO TABLE movie_character
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(movie_character_name);

--
-- ACTOR TABLE
--

CREATE TABLE IF NOT EXISTS actor
  (
    actor_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    actor_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (actor_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/alexandracarey/Documents/Third_Semester/664/Final_Project/disney/output/disney_actor.csv'
INTO TABLE actor
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(actor_name);

--
-- GENRE TABLE
--

CREATE TABLE IF NOT EXISTS genre
  (
    genre_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    genre_name VARCHAR(45) NOT NULL UNIQUE,
    PRIMARY KEY (genre_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/alexandracarey/Documents/Third_Semester/664/Final_Project/disney/output/disney_genre.csv'
INTO TABLE genre
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(genre_name);

--
-- DIRECTOR TABLE
--

CREATE TABLE IF NOT EXISTS director
  (
    director_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    director_name VARCHAR(45) NOT NULL UNIQUE,
    PRIMARY KEY (director_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/alexandracarey/Documents/Third_Semester/664/Final_Project/disney/output/disney_director.csv'
INTO TABLE director
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(director_name);


--
-- TEMPORARY TABLE
--

CREATE TABLE IF NOT EXISTS temp_movie
  (
    -- id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    -- movie_title VARCHAR(150) NULL,
    -- director_name VARCHAR(100) NULL,
    -- genre VARCHAR(45) NULL,
    -- PRIMARY KEY (id)
    movie_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    movie_title VARCHAR(150) NOT NULL UNIQUE,
    director_name VARCHAR(100) NULL,
    release_date VARCHAR(50) NOT NULL,
    genre VARCHAR(45) NULL,
    song VARCHAR(140) NULL,
    total_gross INTEGER NULL,
    inflation_gross INTEGER NULL,
    PRIMARY KEY (movie_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/alexandracarey/Documents/Third_Semester/664/Final_Project/disney/source/disney_movies_master.csv'
INTO TABLE temp_movie
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (movie_title, director_name, release_date, genre, song, total_gross, inflation_gross)

  SET movie_title = IF(movie_title  = '', NULL, movie_title),
  director_name = IF(director_name = '', NULL, director_name),
  release_date = IF(release_date = '', NULL, release_date),
  genre = IF(genre = '', NULL, genre),
  song = IF(song = '', NULL, song),
  total_gross = IF(total_gross = '', NULL, total_gross),
  inflation_gross= IF(inflation_gross = '', NULL, inflation_gross);

--
-- MOVIE TABLE
--

CREATE TABLE IF NOT EXISTS movie
  (
    movie_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    movie_title VARCHAR(150) NOT NULL UNIQUE,
    director_id INTEGER NOT NULL,
    release_date VARCHAR(50) NOT NULL,
    genre_id INTEGER NULL,
    song VARCHAR(150) NULL,
    total_gross INTEGER NULL,
    inflation_gross INTEGER NULL,
    PRIMARY KEY (movie_id),
    FOREIGN KEY (director_id) REFERENCES director(director_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
   )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


INSERT IGNORE INTO movie
  (
	  movie_id, 
    movie_title,
    director_id,
    release_date,
    genre_id,
    song,
    total_gross,
    inflation_gross
  )
SELECT temp_movie.movie_id, temp_movie.movie_title, director.director_id, temp_movie.release_date, genre.genre_id, temp_movie.song, temp_movie.total_gross, temp_movie.inflation_gross 
FROM temp_movie
    LEFT JOIN director
        ON TRIM(director.director_name) = TRIM(temp_movie.director_name)
    LEFT JOIN genre
        ON TRIM(genre.genre_name) = TRIM(temp_movie.genre);


DROP TABLE temp_movie;


--
-- CONNECTOR TABLE
--

CREATE TABLE IF NOT EXISTS temp_chars
  (
  	char_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  	movie_character_name VARCHAR(200) NOT NULL,
  	actor_name VARCHAR(150) NOT NULL,
    movie_title VARCHAR(150) NOT NULL,
    PRIMARY KEY (char_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/alexandracarey/Documents/Third_Semester/664/Final_Project/disney/output/disney_voice_actors_trimmed.csv'
INTO TABLE temp_chars
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (movie_character_name, actor_name, movie_title);


--
-- CREDIT TABLE (connector)
--


CREATE TABLE IF NOT EXISTS credit
  (
	credit_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	movie_character_id INTEGER NULL,
	actor_id INTEGER NULL,
	movie_id INTEGER NULL,
	-- motive_id INTEGER NOT NULL,
	PRIMARY KEY (credit_id),
    FOREIGN KEY (movie_character_id) REFERENCES movie_character(movie_character_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actor(actor_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
    ON DELETE CASCADE ON UPDATE CASCADE
    -- FOREIGN KEY (motive_id) REFERENCES motive(motive_id)
    -- ON DELETE RESTRICT ON UPDATE CASCADE,
   )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


INSERT IGNORE INTO credit
  (
    movie_character_id,
    -- motive_id,
    actor_id,
    movie_id
  )
SELECT movie_character.movie_character_id, actor.actor_id, movie.movie_id
FROM temp_chars
    LEFT JOIN movie_character
        ON TRIM(temp_chars.movie_character_name) = TRIM(movie_character.movie_character_name)
    LEFT JOIN actor
        ON TRIM(temp_chars.actor_name) = TRIM(actor.actor_name)
    LEFT JOIN movie
        ON TRIM(temp_chars.movie_title) = TRIM(movie.movie_title);


DROP TABLE temp_chars;