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
* 1 - 5 : back to home menu  
#### -------------- CONTRACTS -------------------
* 2 - 1 : creation of contracts
* 2 - 2 : view/modification of contracts
* 2 - 3 : sign contracts
* 2 - 4 : filter contracts
* 2 - 4 - 1 : non signed contracts
* 2 - 4 - 2 : non payed contracts
* 2 - 5 : back to home menu  
#### -------------- EVENTS ----------------------
* 3 - 1 : creation of events
* 3 - 2 : assignation of events
* 3 - 3 : view/modification of events
* 3 - 4 : filter events
* 3 - 4 - 1 : non assigned events
* 3 - 4 - 2 : events in progress or incoming
* 3 - 4 - 3 : my assigned events
* 3 - 5 : back to home menu  
#### ------------- EMPLOYEES --------------------
* 4 - 1 : creation of employees
* 4 - 2 : view/modification of employees
* 4 - 3 : delete employees

## detailled menus
### Base menu

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/fb439c5f-9214-4949-a363-04c58367e7ad">
</p>

### 1 - CUSTOMERS

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/e23b8a34-0d87-4bac-aa9c-96fa6a026160">
</p>

### 1 - 1 creation of customers
Only commercials can create new customers:
* name         : name of the customer (255 caracters max)
* email        : email of the customer (restricted to standard form of email, 255 caracters max), should be unique
* phone number : not mandatory, phone number of the customer (restricted to standard form of phone number)
* company name : company name of the customer (max 255 caracters)
### 1 - : view and modification of customers
-> According to your access rights, you can view or modify customers values:
* select customer by name, if you don't know press [ENTER] to choose by list
* if your rights access permit, you will be invited to modify values of the customer, else
  just view information
### 1 - 3 (soft) delete customers
-> According to your access rights, you can (soft) delete customers:
* select an customer by name, if you don't know press [ENTER] to choose by list
* Confirm, or not, the deletion
### 1 - 5 back to main menu
------------------------------------------------------------------------------------------------------------------
### 2 - CONTRACTS

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/75c77daa-7273-49d7-b959-dee33c74b9c9">
</p>

### 2 - 1 creation of contracts
-> Only Employees of management department can create new contracts
* Price    : price of the contract
* Due      : amount due (should be less than price), [ENTER] = 0
* Signed   : sign contract "o" or "n"? (if no you will can do it later), [ENTER] = "n"
* Customer : choose customer to associate to this contract (by entry of list)
### 2 - 2 view and modification of contracts
-> According to your access rights, you can view or modify customers values:
* select contract by number, if you don't know press [ENTER] to choose by list
* if your rights access permit, you will be invited to modify values of the contract, else
  just view information
### 2 - 3 sign contracts
* select contract by number or if you don't know by selecting in a list (inly not signed contract will appear)
  (considering that if a contract is signed, you are unable to modify it, just logic ;-)
* confirm signature
### 2 - 4 filter contracts

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/0c870e82-98f3-4c70-b9e1-2b9527bee9f7">
</p>

-> Only commercials can access to this menu
### 2 - 4 - 1 display signed contracts
* display all contracts with status = "NOT SIGNED"
### 2 - 4 - 1 display signed not fully payed
* display all contracts with a du other than zero
### 2 - 5 back to main menu
------------------------------------------------------------------------------------------------------------------
### 3 - EVENTS

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/9ab57616-ab77-41ea-8fea-8986920c9c89">
</p>

### 3 - 1 creation of events
-> Only commercials can access to this menu
* select contract by number, if you don't know press [ENTER] to choose by list
  (considering that only signed contracts and not associated to an event appear and allowed)
* enter start date of the event (format : 04/06/23 13:00)
* enter end date of the event (superior to start date)
* location of the event (format : [street with or without number], [postal code], [town])
* number of attendees
* notes : not mandatory, if you want some notes, 1000 caracters max
### 3 - 2 assign events
-> Only management department employees can access to this menu
* select event number by entry, if you don't know press [ENTER] to choose by list
  (considering that only events not associated will appear and allowed)
* select employee by username, if you don't know press [ENTER] to choose by list
### 3 - 3 view and modification of events
->  Only support department employees can edit their own events, others can read only
* select event by number, if you don't know press [ENTER] to choose by list
### 3 - 4 filter events

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/297f376e-ca44-4286-a82e-4ce58714d102">
</p>

### 3 - 4 - 1 events not assigned
-> only management can access to this menu
* display all event where no support employee associated
### 3 - 4 - 2 event in progress (end date not yet passed)
-> only management can access to this menu
* display all event to come or in progress
### 3 - 4 - 3 event associated to support employee loggedin the application
-> only support employee can access to this menu
* display all events associated to the loggedin employee
------------------------------------------------------------------------------------------------------------------
### 4 - EMPLOYEES

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/818fa4f7-5575-4816-ac33-7b6bce54a428">
</p>

### 4 - 1 creation of employees
-> Only management department can access to this menu
* username    : the username of the employee he will use to connect in the application
* password    : 8 caracters min, at least one number, at least one letter, at least on special caracter
* email       : bad format of the email will be rejected
* department  : select department of the user by choosing in list
### 4 - 2 view modification of employees
-> According to your access rights, you can view or modify customers values:
* select employee by username, if you don't know press [ENTER] to choose by list
* if your rights access permit, you will be invited to modify values of the contract, else
  just view information
### 4 - 3 (soft) delete employee
-> According to your access rights, you can (soft) delete employees:
* select an customer by name, if you don't know press [ENTER] to choose by list
* Confirm, or not, the deletion
------------------------------------------------------------------------------------------------------------------
## Test
You can launch integrity test with this command : `coverage run -m unittest discover -v .\tests\unit_tests\`

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/6fc7cc11-e2de-40ae-b303-d3a00298b87f">
</p>

To check coverage, execute this command : `coverage report`

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/d5e534b3-6e41-4486-993a-81fe7404def3">
</p>

## Features
When launching the application for the first time, there is 4 departmens autocreated + 4 employees with same names:
* superadmin : access to all menus and all features
* commercial : used to manage customers and events
* management : used to manage employees, contracts and assignation of events to an support employee
* support    : used to be assigned to an event, these can also modify their own event  

If you want to autocreate employees, contracts and events, just enter "666" at the home menu :-)
(in that way you can play with samples to navigate in menus...)






