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

--4.
USE user_management;

ALTER TABLE feature MODIFY modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
ALTER TABLE requirement  MODIFY modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
ALTER TABLE design MODIFY modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
ALTER TABLE implementation MODIFY modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
ALTER TABLE testcase MODIFY modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

--5.
-- Run this for feature, requirement, design, implementation, testcase
ALTER TABLE feature DROP COLUMN created;
ALTER TABLE requirement DROP COLUMN created;
ALTER TABLE design DROP COLUMN created;
ALTER TABLE implementation DROP COLUMN created;
ALTER TABLE testcase DROP COLUMN created;


--6.
---- 1. Select the database
USE user_management;

---- 2. Add the new user_id column. Allow NULLs for now so we can populate it.
ALTER TABLE login_history ADD COLUMN user_id INT NULL AFTER id; -- Position after id (optional)

---- 3. Populate the new user_id column based on the existing username.
-- This matches usernames between login_history and users table.
-- Run this command carefully. If a username in login_history doesn't exist
-- in the users table anymore, that row's user_id will remain NULL.
UPDATE login_history lh
JOIN users u ON lh.username = u.username
SET lh.user_id = u.id
WHERE lh.user_id IS NULL; -- Only update rows that haven't been processed

-- Check if any rows failed to update (optional):
-- SELECT * FROM login_history WHERE user_id IS NULL;
-- If you find rows with NULL user_id, you may need to manually fix them or decide
-- if that history record is still valid (e.g., if the user was deleted).

---- 4. Add the Foreign Key constraint to link user_id to the users table.
-- This enforces the relationship.
ALTER TABLE login_history
ADD CONSTRAINT fk_user_login
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE; -- Optional: ON DELETE CASCADE removes history if the user is deleted.
                   -- Use ON DELETE SET NULL if you want to keep history but set user_id to NULL.
                   -- Use ON DELETE RESTRICT (or omit ON DELETE) to prevent user deletion if history exists.

---- 5. Modify the user_id column to require a value (NOT NULL).
-- Do this ONLY AFTER successfully populating existing records in step 3.
-- If some records have NULL user_id after step 3, this command will fail
-- until those NULLs are resolved (either update them or delete those history rows).
ALTER TABLE login_history MODIFY COLUMN user_id INT NOT NULL;
