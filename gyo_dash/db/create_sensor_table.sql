
CREATE TABLE sensor_data (
	ID int NOT NULL AUTO_INCREMENT,
	Humidity float,
	Temperature float,
	ts DATETIME,
	PRIMARY KEY (ID)
);