DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS projects;

CREATE TABLE projects(
  id_project INT UNSIGNED AUTO_INCREMENT,
  hashtag VARCHAR(50) UNIQUE,
  num_votes INT UNSIGNED DEFAULT 0,
  PRIMARY KEY(id_project)
);

CREATE TABLE participants(
 email VARCHAR(100),
 hasVoted TINYINT UNSIGNED DEFAULT 0,
 hashtag VARCHAR(50),
 PRIMARY KEY(email),
 FOREIGN KEY(hashtag) REFERENCES projects(hashtag)
);