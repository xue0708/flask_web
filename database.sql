CREATE DATABASE Test_system;

USE Test_system;

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS alembic_version;

CREATE TABLE alembic_version
(
	version_num varchar(32) NOT NULL,
	PRIMARY KEY (version_num)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO alembic_version(version_num) VALUES ('d0a35a10500d');

DROP TABLE IF EXISTS user;

CREATE TABLE user 
(
	id int(11) NOT NULL AUTO_INCREMENT,
	username varchar(64) DEFAULT NULL,
	password_hash varchar(128) DEFAULT NULL,
	maxdx int(8) DEFAULT NULL,
	maxdy int(8) DEFAULT NULL,
	maxdz int(8) DEFAULT NULL,
	maxgx int(8) DEFAULT NULL,
	maxgy int(8) DEFAULT NULL,
	maxgz int(8) DEFAULT NULL,
	last_seen datetime DEFAULT NULL,
	PRIMARY KEY (id),
	UNIQUE KEY ix_user_username (username)
)ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE data1 
(
	id int(11) NOT NULL AUTO_INCREMENT,
	timetag datetime DEFAULT NULL,
	dx decimal(30,15) DEFAULT NULL,
	dy decimal(30,15) DEFAULT NULL,
	dz decimal(30,15) DEFAULT NULL,
	gx decimal(30,15) DEFAULT NULL,
	gy decimal(30,15) DEFAULT NULL,
	gz decimal(30,15) DEFAULT NULL,
	PRIMARY KEY (id)
)ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE data2
(
	id int(11) NOT NULL AUTO_INCREMENT,
	timetag datetime DEFAULT NULL,
	dx decimal(30,15) DEFAULT NULL,
	dy decimal(30,15) DEFAULT NULL,
	dz decimal(30,15) DEFAULT NULL,
	gx decimal(30,15) DEFAULT NULL,
	gy decimal(30,15) DEFAULT NULL,
	gz decimal(30,15) DEFAULT NULL,
	PRIMARY KEY (id)
)ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

