CREATE TABLE votes (
vote_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
item_id INT(6) NOT NULL,
rating INT(5) NOT NULL DEFAULT 10,
created_by_ID INT(6) UNSIGNED DEFAULT 2,
created_date TIMESTAMP
)
