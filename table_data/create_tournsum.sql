DROP TABLE pga.tournsum;
CREATE TABLE pga.tournsum (
id INT AUTO_INCREMENT primary key NOT NULL,
t_id char(3),
shortname char(25),
year INT,
plyr_id char(5),
finposvalue INT,
primarytour char(1),
plyr_name char(23),
money INT,
finposnum INT,
totalscore INT,
eventfedexpoints INT,
plyr_name_last_first char(24),
relparscrtot INT);
