DROP TABLE pga.tournaments;
CREATE TABLE pga.tournaments (
id INT AUTO_INCREMENT primary key NOT NULL,
t_id char(3),
name char(25),
year INT, 
fullname char(66));
