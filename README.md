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

## Utilisation
See bellow all menus available:
#### --------------- CUSTOMERS ------------------
* 1 - 1 : creation of customers
* 1 - 2 : view/modification of customers
* 1 - 3 : delete customers
* 1 - 6 : back to home menu  
#### -------------- CONTRACTS -------------------
* 2 - 1 : creation of contracts
* 2 - 2 : view/modification of contracts
* 2 - 3 : delete contracts
* 2 - 4 : sign contracts
* 2 - 5 : filter contracts
* 2 - 5 - 1 : non signed contracts
* 2 - 5 - 2 : non payed contracts
* 2 - 6 : back to home menu  
#### -------------- EVENTS ----------------------
* 3 - 1 : creation of events
* 3 - 2 : assignation of events
* 3 - 3 : view/modification of events
* 3 - 4 : delete events
* 3 - 5 : filter events
* 3 - 5 - 1 : non assigned events
* 3 - 5 - 2 : events in progress or incoming
* 3 - 5 - 3 : my assigned events
* 3 - 6 : back to home menu  
#### ------------- EMPLOYEES --------------------
* 4 - 1 : creation of employees
* 4 - 2 : view/modification of employees
* 4 - 3 : delete employees

## detailled menus
### 1 - 1 : creation of customers
In this menu, commercials can create new customers:
* name         : name of the customer (255 caracters max)
* email        : email of the customer (restricted to standard form of email, 255 caracters max)
* phone number : phone number of the customer (restricted to standard form of phone number)
* company name : company name of the customer (max 255 caracters)
### 1 - 2 : view and modification of customers
In this menu, according to your access rights, you can view or modify customers values:
* select an customer by name or if you don't know the name by selecting in a list.
* if your rights access permit, you will be invited to modify values of the customer, else
  just view information
### 1 - 3 : delete customers
In this menu, according to your access rights, you can delete customers:
* select an customer by name or if you don't know the name by selecting in a list.




