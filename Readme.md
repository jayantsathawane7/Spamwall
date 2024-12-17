
# Steps to Run the SpamShield Project
## Pre-Steps
### Install MySQL Server and Client:

Install MySQL:
```
sudo apt update
sudo apt install mysql-server mysql-client
```

Ensure the MySQL service is running:

```
sudo service mysql start
```

Note : MySQL should run on port 3306.

### Create the Database:
Log in to MySQL:
```
mysql -uroot -padmin123 -h127.0.0.1
```

Create the database:
```
CREATE DATABASE spamwalldb;
```

## Project Setup Steps

### Extract the ZIP File:
Extract the spamwall.zip file into your desired directory.

```
unzip spamwall.zip -d ~/projects
cd ~/projects/spamwall
```

### Set Up a Virtual Environment:
Create and activate a Python virtual environment:
```
python3 -m venv env
source env/bin/activate
```

### Install Python Dependencies:
Install the required dependencies from requirements.txt:
```
pip install -r requirements.txt
```

### Apply Migrations:
Generate migrations for database models:
```
python manage.py makemigrations
python manage.py migrate
```

### Run the Development Server:
Start the Django server on port 8080:
```
python manage.py runserver 8080
```

## Access the Application
Open your browser and navigate to: http://127.0.0.1:8080/.

