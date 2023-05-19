use db;

CREATE TABLE IF NOT EXISTS apartment (
    ApartmentID int not null AUTO_INCREMENT,  
    title VARCHAR(255),
    url VARCHAR(255),
    PRIMARY KEY (ApartmentID)
);
