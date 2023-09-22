<p align="center">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/d65dd94f-dacd-450c-aaf2-83b1533e5b55">
</p>

# Projet12OC
Back-end using Python and SQL database.
For this project I used MySql 8.0.34 and Python 3.11.5

## Installation
* Clone repository: `git clone https://github.com/LeChat76/Projet12OC.git`  
* Enter in created folder: `cd Projet12OC`  
* Create virtual environment: `python -m venv .venv`  
* Activate environment:  
    * for Linux `source .venv/bin/activate`  
    * for Windows `.\.venv\Scripts\activate`  
* Install the necessary libraries: `pip install -r requirements.txt` 
* Run the webserver : `python .\main.py` 

## Configuration
* Please replace values in `contants\database.py` with the values of your SQL server:
    * DB_USER     : the username for accessing to your SQL database
    * DB_PASSWORD : the password associated to the DB_USER
    * DB_HOST     : the IP Address of the SQL server (if on your own computer, your can use `localhost`)
    * DB_NAME     : the name of the database you created on your SQL server (for example : `CREATE DATABASE epicevents;`)

See bellow all menus available:
  
--------------- CUSTOMERS ------------------
* 1 - 1 : creation of customers
* 1 - 2 : vue/modification of customers
* 1 - 3 : delete customers
* 1 - 4 : back to home menu  
-------------- CONTRACTS -------------------
* 2 - 1 : creation of contracts
* 2 - 2 : vue/modification of contracts
* 2 - 3 : delete contracts
* 2 - 4 : sign contracts
* 2 - 5 : back to home menu  
-------------- EVENTS ----------------------
* 3 - 1 : creation of events
* 3 - 2 : assignation of events
* 3 - 3 : voir/modification of events
* 3 - 4 : delete events
* 3 - 5 : back to home menu  

To be continued ;-)

