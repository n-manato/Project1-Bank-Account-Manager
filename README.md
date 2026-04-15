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