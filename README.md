# Bank Account Manager

## Project Overview
This project is an expanded version of Lab 9.

The original Lab 9 focused on object-oriented programming with `Account` and `SavingAccount` classes. This project extends that idea into a full PyQt6 GUI banking application.

The program allows users to create and manage multiple bank accounts through a graphical interface. Users can deposit money, withdraw money, transfer money between accounts, view transaction history, and save or load account data using CSV files.

## Features
- PyQt6 graphical user interface
- Multiple account management
- Account creation
- Deposit function
- Withdraw function
- Transfer function
- Transaction history display
- CSV save and load
- Input validation
- Exception handling
- Object-oriented design with inheritance
- User registration and login
- Password hashing with salt

## Account Types

### Account
A basic bank account that supports deposits and withdrawals.

### SavingAccount
A savings account based on Lab 9.  
It keeps a minimum balance of 100 dollars.  
Interest is applied after every 5 successful deposits.

### CheckingAccount
A new account type added for this project.  
It allows withdrawals, and after a certain number of withdrawals, a fee may be charged.

## Files
- `main.py`  
  Starts the application.

- `gui.py`  
  Contains the PyQt6 GUI code.

- `accounts.py`  
  Contains the `Account`, `SavingAccount`, and `CheckingAccount` classes.

- `bank.py`  
  Manages accounts and transaction history.

- `storage.py`  
  Handles CSV saving and loading.

- `auth.py`  
  Handles user registration, password hashing, and login checking.

- `login.py`  
  Contains the PyQt6 login and register dialog.

## Concepts Used
This project uses the following programming concepts:
- Classes and objects
- Inheritance
- Data hiding
- File handling
- Exception handling
- Input validation
- Modular code organization
- GUI programming with PyQt6

## Requirements
- Python 3
- PyQt6

## Installation
Install PyQt6 before running the program:

```bash
pip install PyQt6

## Login Feature
The program now starts with a login window.

Users can:
- Register a new username and password
- Log in with an existing account
- Open the bank manager only after a successful login

User data is saved in `users.csv`.  
Passwords are not saved as plain text. The program saves a salted SHA-256 password hash.

## How to Run

```bash
python main.py
```

First, click **Register** to create a user.  
Then click **Login** to open the main bank manager window.
