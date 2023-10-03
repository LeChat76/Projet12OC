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
This application need two accounts : `admin_epicevents` and `guest_epicevents`.
User `admin_epicevents` is used to create table and record when launching the application for the first time.
User `guest_epicevents` is used to use the database. Guest should have restricted access to the database (DROP commands
should be fordiben) (both user with password 'Toto1234!' for this demonstration).
Logged users will be connected to the database with limited MySql account. In that way, they could never delete tables
or in worst case : the whole database!
 * from MySql CLI, create database : `CREATE DATABASE epicevents;`
 * select database                 : `USE epicevents;`
 * create user `admin_epicevents`  : `CREATE USER 'admin_epicevents' IDENTIFIED BY 'Toto1234!';`
 * grant all privileges            : `GRANT ALL PRIVILEGES ON epicevents.* TO 'admin_epicevents';`
 * create user `guest_epicevents`  : `CREATE USER 'guest_epicevents' IDENTIFIED BY 'Toto1234!';`
 * grant limited privileges        : `GRANT SELECT, INSERT, UPDATE on epicevents.* to 'guest_epicevents';`
 * update privileges               : `FLUSH PRIVILEGES;`
You can modify those 2 options if needed:
  * DB_HOST     : the IP Address of the SQL server (if on your own computer, your can use `localhost`)
  * DB_NAME     : the name of the database you created on your SQL server

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
* 4 - 4 : générer token

## detailled menus
### Base menu

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/fb439c5f-9214-4949-a363-04c58367e7ad">
</p>

### 1 - CUSTOMERS

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/e23b8a34-0d87-4bac-aa9c-96fa6a026160">
</p>

<u>**Legend**</u> : **at the end of each title menu will appear 3 letters : C(ommercial), M(anagement) and S(upport).**  
**This corresponds to the type of employee authorized to access this menu.**  
**When star '*' after letter : mean access in write mode (creation + modification).**  
**(superadmin is authorized to all menus)**  

### 1 - 1 creation of customers(M*)
* name         : name of the customer (255 caracters max)
* email        : email of the customer (restricted to standard form of email, 255 caracters max), should be unique
* phone number : not mandatory, phone number of the customer (restricted to standard form of phone number)
* company name : company name of the customer (max 255 caracters)
### 1 - : view and modification of customers(M*CS)
* select customer by name, if you don't know press [ENTER] to choose by list
* if your rights access permit, you will be invited to modify values of the customer, else
  just view information
### 1 - 5 back to main menu
------------------------------------------------------------------------------------------------------------------
### 2 - CONTRACTS

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/75c77daa-7273-49d7-b959-dee33c74b9c9">
</p>

### 2 - 1 creation of contracts(M*)
* Price    : price of the contract
* Due      : amount due (should be less than price), [ENTER] = 0
* Signed   : sign contract "o" or "n"? (if no you will can do it later), [ENTER] = "n"
* Customer : choose customer to associate to this contract (by entry of list)
### 2 - 2 view and modification of contracts(M*CS)
* select contract by number, if you don't know press [ENTER] to choose by list
* if your rights access permit, you will be invited to modify values of the contract, else
  just view information
### 2 - 3 sign contracts(M*)
* select contract by number or if you don't know by selecting in a list (inly not signed contract will appear)
  (considering that if a contract is signed, you are unable to modify it, just logic ;-)
* confirm signature
### 2 - 4 filter contracts
<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/0c870e82-98f3-4c70-b9e1-2b9527bee9f7">
</p>

### 2 - 4 - 1 display signed contracts(C)
* display all contracts with status = "NOT SIGNED"
### 2 - 4 - 1 display signed not fully payed(C)
* display all contracts with a du other than zero
### 2 - 5 back to main menu
------------------------------------------------------------------------------------------------------------------
### 3 - EVENTS

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/9ab57616-ab77-41ea-8fea-8986920c9c89">
</p>

### 3 - 1 creation of events(C*)
* select contract by number, if you don't know press [ENTER] to choose by list
  (considering that only signed contracts and not associated to an event appear and allowed)
* enter start date of the event (format : 04/06/23 13:00)
* enter end date of the event (superior to start date)
* location of the event (format : [street with or without number], [postal code], [town])
* number of attendees
* notes : not mandatory, if you want some notes, 1000 caracters max
### 3 - 2 assign events(M*)
* select event number by entry, if you don't know press [ENTER] to choose by list
  (considering that only events not associated will appear and allowed)
* select employee by username, if you don't know press [ENTER] to choose by list
### 3 - 3 view and modification of events(CMS*)
->  Only support department employees can edit their own events, others can read only
* select event by number, if you don't know press [ENTER] to choose by list
### 3 - 4 filter events


<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/297f376e-ca44-4286-a82e-4ce58714d102">
</p>

### 3 - 4 - 1 events not assigned(M)
* display all event where no support employee associated
### 3 - 4 - 2 event in progress(M)
* display all event to come or in progress
### 3 - 4 - 3 event associated to support employee loggedin the application(S)
* display all events associated to the loggedin support employee
------------------------------------------------------------------------------------------------------------------
### 4 - EMPLOYEES

<p align="left">
    <img alt="logo" src="https://github.com/LeChat76/Projet12OC/assets/119883313/2864c06c-9627-4e5b-a436-f4f2372065fe">
</p>

### 4 - 1 creation of employees(M*)
* username    : the username of the employee he will use to connect in the application
* password    : 8 caracters min, at least one number, at least one letter, at least on special caracter
* email       : bad format of the email will be rejected
* department  : select department of the user by choosing in list
### 4 - 2 view modification of employees(CM*S)
-> According to your access rights, you can view or modify customers values:
* select employee by username, if you don't know press [ENTER] to choose by list
* if your rights access permit, you will be invited to modify values of the contract, else
  just view information
### 4 - 3 (soft) delete employee(M*)
* select an employee by name, if you don't know press [ENTER] to choose by list
* Confirm, or not, the deletion
### 4 - 4 generate token
-> only management department employees and superadmin account can access to this menu
* select an employee by name, if you don't know press [ENTER] to choose by list
* file `token.tkn` will be created in root folder of this application. This file contain
a token, the same will be stored in the database associated to the concerned employee.
Now you can log to the application by typing : `python.exe .\main.py --token` to auto connect

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
* When launching the application for the first time, there is 4 departmens autocreated + 4 employees with same names:
  - superadmin : access to all menus and all features
  - commercial : used to manage customers and events
  - management : used to manage employees, contracts and assignation of events to an support employee
  - support    : used to be assigned to an event, these can also modify their own event  

* If you want to autocreate employees, contracts and events, just enter "666" at the home menu :-)  
(in that way you can 'play' with samples to navigate in menus...).

* Management of the login with token

* To avoid SQL injections, I didn't use any raw SQL queries, only the secure SQL Alchemy commands.  
In addition, once the tables have been created by my application, all other queries are executed
by a limited user account (no DROP command allowed).






