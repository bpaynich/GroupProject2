CREATE DATABASE season_stats_db;
USE  season_stats_db;


CREATE TABLE arena_name (
  id INT PRIMARY KEY,
  arena_name TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  zipcode TEXT,
  latitude INT,
  longitude INT
);

CREATE TABLE historical_arena (
  id INT PRIMARY KEY,
  year INT,
  arena_name TEXT,
  team_name TEXT
);
