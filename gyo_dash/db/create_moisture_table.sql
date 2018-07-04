
CREATE TABLE moisture_state(
    ID int NOT NULL AUTO_INCREMENT,
    moisture ENUM ('LOW', 'HIGH'),
    create_time DATETIME,
    PRIMARY KEY (ID)
)