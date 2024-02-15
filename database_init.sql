CREATE SCHEMA IF NOT EXISTS funnyapi;
USE funnyapi;

CREATE TABLE IF NOT EXISTS user (
    user_id SMALLINT UNSIGNED AUTO_INCREMENT,
    username VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    is_banned BOOLEAN DEFAULT 0,

    PRIMARY KEY (user_id),
    INDEX idx_username (username)
);

CREATE TABLE IF NOT EXISTS joke (
    joke_id SMALLINT UNSIGNED AUTO_INCREMENT,
    user_id SMALLINT UNSIGNED,
    title VARCHAR(20) NOT NULL,
    body VARCHAR(500) NOT NULL,
    likes_count SMALLINT NOT NULL DEFAULT 0,
    created timestamp DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (joke_id),
    FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE IF NOT EXISTS category (
    category_id SMALLINT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(20) UNIQUE NOT NULL,

    PRIMARY KEY (category_id)
);

CREATE TABLE IF NOT EXISTS joke_category (
    joke_id SMALLINT UNSIGNED,
    category_id SMALLINT UNSIGNED,

    PRIMARY KEY (joke_id, category_id),
    FOREIGN KEY (joke_id) REFERENCES joke (joke_id),
    FOREIGN KEY (category_id) REFERENCES category (category_id)
);
