DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS projects;

CREATE TABLE projects(
  id_project INT UNSIGNED AUTO_INCREMENT,
  hashtag VARCHAR(50) UNIQUE,
  team VARCHAR(100) UNIQUE,
  num_votes INT UNSIGNED DEFAULT 0,
  social_votes INT UNSIGNED DEFAULT 0,
  PRIMARY KEY(id_project)
);

CREATE TABLE participants(
 email VARCHAR(100),
 name VARCHAR(50),
 hasVoted TINYINT UNSIGNED,
 hashtag VARCHAR(50),
 PRIMARY KEY(email),
 FOREIGN KEY(hashtag) REFERENCES projects(hashtag)
);