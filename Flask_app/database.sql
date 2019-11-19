CREATE DATABASE jdh_system;

USE jdh_system;

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS alembic_version;

CREATE TABLE alembic_version
(
	version_num varchar(32) NOT NULL,
	PRIMARY KEY (version_num)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO alembic_version(version_num) VALUES ('d0a35a10500d');

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS camera_information;
DROP TABLE IF EXISTS abnormaldetect;

CREATE TABLE user 
(
	id int(11) NOT NULL AUTO_INCREMENT,
	username varchar(64) DEFAULT NULL,
	email varchar(120) DEFAULT NULL,
	telephone varchar(20) DEFAULT NULL,
	password_hash varchar(128) DEFAULT NULL,
	company varchar(40) DEFAULT NULL,
	last_seen datetime DEFAULT NULL,
	PRIMARY KEY (id),
	UNIQUE KEY ix_user_email (email),
	UNIQUE KEY ix_user_username (username)
)ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE camera_information 
(
	id int(11) NOT NULL AUTO_INCREMENT,
	cameraid int(11) DEFAULT NULL,
	imagepath varchar(120) DEFAULT NULL,
	videopath varchar(120) DEFAULT NULL,
	username varchar(64) DEFAULT NULL,
	last_time datetime DEFAULT NULL,
	PRIMARY KEY (id)
)ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE abnormaldetect
(
	id int(11) NOT NULL AUTO_INCREMENT,
	cameraid int(11) DEFAULT NULL,
	imagepath varchar(120) DEFAULT NULL,
	videopath varchar(120) DEFAULT NULL,
	username varchar(64) DEFAULT NULL,
	last_time datetime DEFAULT NULL, 
	PRIMARY KEY (id)
);
