-- SQL CODE FOR ABOVE CODE:
-- 1. Tabe creation

CREATE DATABASE user_management;

USE user_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user'
);


CREATE TABLE feature (
    id Varchar(50),
    name VARCHAR(255),
    description TEXT,
    created DATETIME,
    modified DATETIME,
    status VARCHAR(50),
    priority VARCHAR(50),
    version VARCHAR(50)
);

CREATE TABLE requirement (
    id Varchar(50),
    name VARCHAR(255),
    description TEXT,
    created DATETIME,
    modified DATETIME,
    status VARCHAR(50),
    priority VARCHAR(50),
    version VARCHAR(50),
    category VARCHAR(255),
    assigned TEXT
);

CREATE TABLE design (
    id Varchar(50),
    name VARCHAR(255),
    description TEXT,
    created DATETIME,
    modified DATETIME,
    status VARCHAR(50),
    priority VARCHAR(255),
    version VARCHAR(50),
    category TEXT
);

CREATE TABLE implementation (
    id Varchar(50),
    name VARCHAR(255),
    description TEXT,
    created DATETIME,
    modified DATETIME,
    status VARCHAR(50),
    language VARCHAR(50),
    loc VARCHAR(50),
    complexity VARCHAR(50),
    developer VARCHAR(255)
);

CREATE TABLE testcase (
    id Varchar(50),
    name VARCHAR(255),
    description TEXT,
    created DATETIME,
    modified DATETIME,
    status TEXT,
    type TEXT,
    prerequisites TEXT,
    expectedresult TEXT,
    actualresult TEXT
);

CREATE TABLE login_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    login_time DATETIME NOT NULL
);

CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




-- 2. Manually Register an Admin Run this SQL command to create an admin user

-- NOTE: In VALUES--> 'admin_user' = "Enter your name" AND 'AdminPassword@123' = "Enter any password you want to set" AND 'admin' = remains as it is 

-- It is required to implement this manually since we have to create the admin first to start registerting other users as well as additional admin if required thorugh application UI itself

INSERT INTO users (username, password, role) 
VALUES ('admin_user', SHA2('AdminPassword@123', 256), 'admin');



-- 3. Alter table to include project id

ALTER TABLE feature ADD COLUMN project_id INT;
ALTER TABLE requirement ADD COLUMN project_id INT;
ALTER TABLE design ADD COLUMN project_id INT;
ALTER TABLE implementation ADD COLUMN project_id INT;
ALTER TABLE testcase ADD COLUMN project_id INT;
