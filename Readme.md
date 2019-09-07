MatD3 database software
=======================

MatD3 is a database and a web application for experimental and theoretical data on solid materials. The objective is to ensure better access and reproducibility of research data and it is intended to be used by any research group wishing to publish their scientific results.

Installation
------------

These are instructions for quickly setting up a local server on your personal computer. For setting up a real server, see the full documentation at https://hybrid3-database.readthedocs.io/en/latest/.

* In the root directory of the project, create a virtual Python environment

   ```
   python -m venv venv
   source venv/bin/activate
   ```

* Install all the requirements

   ```
   pip install -r requirements.txt
   ```

* Define you environment in .env in the root directory of the project

  ```
  cp env.example .env
  # edit .env
  ```

  If you wish to use anything other than the SQLite database, you first need to set up that database (e.g., MariaDB). See https://hybrid3-database.readthedocs.io/en/latest/setup.html for more details.

* Initialize static files and perform database migrations

  ```
  ./manage.py collectstatic
  ./manage.py migrate
  ```

* Create a superuser

  ```
  ./manage.py createsuperuser
  ```

* Start the server

  ```
  ./manage.py runserver
  ```

* Open a web browser and go to http://127.0.0.1:8000/.


Usage
-----

In order to enter data into the database, start by creating a new user (click on Register and follow instructions) or login as the superuser. Next, click on Add Data on the navigation bar in order to submit a data set into the database. Existing data can be viewed by using the Search function on the navigation bar.
