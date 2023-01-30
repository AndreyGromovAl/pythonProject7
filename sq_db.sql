CREATE TABLE Users (
	id_user integer PRIMARY KEY AUTOINCREMENT,
	FullName text,
	Login text,
	Password text,
	Admin boolean
);

CREATE TABLE Offices (
	id_office integer PRIMARY KEY AUTOINCREMENT,
	startlesson time,
	endlesson time,
	officename varchar,
	lessonname varchar,
    Data data,
    Description text
);

CREATE TABLE class (
	id_class integer PRIMARY KEY AUTOINCREMENT,
	classname varchar
);

CREATE TABLE event (
	id integer PRIMARY KEY AUTOINCREMENT,
	title varchar,
	url varchar,
	class varchar,
	start_date timestamp,
	end_date timestamp
);







CREATE TABLE IF NOT EXISTS mainmenu(
    id integer PRIMARY KEY AUTOINCREMENT ,
    title text NOT NULL,
    url   text NOT NULL
);


