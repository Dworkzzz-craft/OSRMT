# OSRMT

# **Steps to Implement this project locally**

1. DB realted info:
   a. First install MYSQL 8.0 database in yuor local system and login using root password and username
   b. Execute the sql give db.sql file to create the database as well necessary tables

2. Logic related info:
   a. Install Python 3.13.2 version
   b. Create a virtual environment
   c. Create a python file named = index.py
   d. Copy and paste the contents of index.py file in this repo to the index.py file you created in your machine
   e. Use 'pip install' to install the necessary modules and libraries which are mentioned in the index.py file.
   f. Run the file and enter the login credentials which you set while executing db.sql contents in your MYSQL software

4. Thats it you are good to go now.


# **Features**

1. Only the admin can add, delete users as well as additional admin if required.
2. Only admin can delete the respective projects.
3. Only the admin can delete the records from the table.
4. Users are not able to register themselves, instead they have to contact the admin to register themselves to acces this application.
5. Users are only able to add, modify the records in the respective table but not able to delete them, the power to delete resides with the admin only.
6. Users are only able to create new projects, but to delete any project resides with the admin only.
