CREATE TABLE dokus (
doku_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(30) NOT NULL,
parent VARCHAR(30) Default "Top", 
created_by_id INT(6) UNSIGNED,
created_date TIMESTAMP
)

