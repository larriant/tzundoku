CREATE TABLE users (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  username varchar(100) NOT NULL UNIQUE,
  email varchar(100) NOT NULL UNIQUE,
  pwdhash varchar(100) NOT NULL,
  PRIMARY KEY ( id )
);
