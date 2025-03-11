
SQL CODE FOR ABOVE CODE:

CREATE DATABASE user_management;

USE user_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    gmail VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE feature (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    created DATETIME,
    modified DATETIME,
    status VARCHAR(50),
    priority VARCHAR(50),
    version VARCHAR(50)
);

CREATE TABLE requirement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    created DATETIME,
    modified DATETIME,
    status VARCHAR(50),
    priority VARCHAR(50),
    type VARCHAR(50),
    source VARCHAR(255),
    rationale TEXT
);

CREATE TABLE design (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    created DATETIME,
    modified DATETIME,
    status VARCHAR(50),
    component VARCHAR(255),
    complexity VARCHAR(50),
    dependencies TEXT
);

CREATE TABLE implementation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    created DATETIME,
    modified DATETIME,
    status VARCHAR(50),
    language VARCHAR(50),
    loc INT,
    complexity VARCHAR(50),
    developer VARCHAR(255)
);

CREATE TABLE testcase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    created DATETIME,
    modified DATETIME,
    status text,
    type Text,
    preconditions text,
    expectedresult text,
    actualresult text
);


1. Update the users Table
Run this SQL command to add the role column:
  
ALTER TABLE users ADD COLUMN role ENUM('admin', 'user') NOT NULL DEFAULT 'user';


2.Manually Register an Admin Run this SQL command to create an admin user:

INSERT INTO users (username, gmail, password, role) 
VALUES ('admin_user', 'admin@example.com', SHA2('AdminPassword123', 256), 'admin');
