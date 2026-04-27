# Bank Account Manager

## Project Overview

Bank Account Manager is a Python desktop application for managing simple bank accounts.

This project is an expanded version of Lab 9.  
The original Lab 9 focused on object-oriented programming with `Account` and `SavingAccount` classes. This project extends that idea into a full PyQt6 GUI banking application.

The program allows users to register, log in, create accounts, deposit money, withdraw money, transfer money between accounts, view transaction history, and save or load account data using CSV files.

## Main Features

- PyQt6 graphical user interface
- Login and user registration system
- Password hashing with salt
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
- Modular code organization

## Login Feature

This project includes a simple login system.

Users can register with a username and password. After registration, users can log in to open the bank account manager.

The program does not save the original password directly. Instead, it saves a hashed password using SHA-256 with a random salt. This is safer than saving plain text passwords.

Login data is saved in a CSV file named `users.csv`.

## Account Types

### Account

A basic bank account.

It supports:

- Deposit
- Withdraw
- Balance checking

### SavingAccount

A savings account based on Lab 9.

It has these rules:

- The account must keep a minimum balance of $100.
- The user cannot withdraw money if the balance would go below $100.
- Interest is applied after every 5 successful deposits.
- The interest rate is 2%.

### CheckingAccount

A checking account added for this project.

It has these rules:

- The account supports normal withdrawals.
- The first 3 withdrawals are free.
- After 3 withdrawals, a $1 fee is charged for each withdrawal.

## Files

### `main.py`

Starts the application.

The program opens the login window first.  
If the login is successful, the main bank account manager window opens.

### `login.py`

Contains the PyQt6 login window.

It allows the user to:

- Enter a username
- Enter a password
- Register a new user
- Log in with an existing user

### `auth.py`

Handles the login system.

It includes:

- User registration
- Password hashing
- Salt generation
- Login checking
- CSV user data storage

### `gui.py`

Contains the main PyQt6 GUI code.

It includes:

- Account creation panel
- Deposit and withdraw panel
- Transfer panel
- Account table
- Transaction history table
- Save and load buttons
- Status messages

### `accounts.py`

Contains the account classes.

It includes:

- `Account`
- `SavingAccount`
- `CheckingAccount`

This file shows inheritance and object-oriented programming.

### `bank.py`

Manages the main bank logic.

It handles:

- Account list
- Transaction history
- Creating accounts
- Finding accounts
- Deposits
- Withdrawals
- Transfers
- Total balance calculation

### `storage.py`

Handles CSV saving and loading.

It saves and loads:

- Account data
- Transaction history

## CSV Files

The program creates CSV files when saving data or registering users.

### `users.csv`

Stores login information.

It stores:

- Username
- Salt
- Hashed password

The plain password is not saved.

### `accounts.csv`

Stores bank account data.

It stores:

- Account type
- Account name
- Balance
- Deposit count
- Withdrawal count

### `transactions.csv`

Stores transaction history.

It stores:

- Date and time
- Action
- Account
- Details
- Amount
- Result

## Program Flow

1. The user runs `main.py`.
2. The login window opens.
3. The user registers or logs in.
4. If the login is successful, the main bank app opens.
5. The user creates a bank account.
6. The user can deposit, withdraw, or transfer money.
7. The transaction history updates after each action.
8. The user can save account and transaction data to CSV files.
9. The user can load saved CSV data later.

## Concepts Used

This project uses these programming concepts:

- Classes and objects
- Inheritance
- Encapsulation
- Data hiding
- GUI programming
- File handling
- CSV reading and writing
- Password hashing
- Input validation
- Exception handling
- Modular programming

## Requirements

- Python 3
- PyQt6

## Installation

Install PyQt6 before running the program:

```bash
pip install PyQt6