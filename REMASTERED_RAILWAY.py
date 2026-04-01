import csv
import pandas as pd
import numpy as np
import sys
import random
import matplotlib.pyplot as plt
import os

# Constants
TRAIN_CSV = r"D:\c\csv2.csv"
RESERVATION_CSV = r"D:\c\csv1.csv"
CREDENTIALS_CSV = "user_credentials.csv"

# Load & Save User Credentials
def load_user_credentials():
    credentials = {}
    try:
        with open(CREDENTIALS_CSV, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    username, password = row
                    credentials[username] = password
    except FileNotFoundError:
        pass
    return credentials

def save_user_credentials(credentials):
    with open(CREDENTIALS_CSV, mode="w", newline="") as file:
        writer = csv.writer(file)
        for username, password in credentials.items():
            writer.writerow([username, password])

# Authentication Functions
def register(credentials):
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    if username in credentials:
        print("Username already exists.")
    else:
        credentials[username] = password
        save_user_credentials(credentials)
        print("Registration successful!")

def login(credentials):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if credentials.get(username) == password:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False

# Menu Option Functions
def handle_option_1(df):
    print(df)
    sno = int(input("Enter s.no: "))
    train_no = int(input("Enter train number: "))
    train_name = input("Enter train name: ")
    start = input("Enter start station: ")
    end = input("Enter end station: ")
    df.loc[sno] = [train_no, train_name, start, end]
    df.to_csv(TRAIN_CSV)
    print("Train added successfully!")

def handle_option_2(df):
    print(df)
    sno = int(input("Enter s.no to remove: "))
    if sno in df.index:
        df.drop(sno, inplace=True)
        df.to_csv(TRAIN_CSV)
        print("Train removed successfully.")
    else:
        print("Invalid s.no")

def handle_option_3(lf):
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    way_from = input("Enter way from station: ")
    way_to = input("Enter way to station: ")
    pnr_no = random.randint(111111, 999999)
    fare = random.randint(1000, 3500)
    lf.loc[pnr_no] = [name, age, way_from, way_to, 'y', fare]
    lf.to_csv(RESERVATION_CSV)
    print(f"Reservation Successful! Your PNR_NO: {pnr_no}")

def handle_option_4(lf):
    print("All Reservations:")
    print(lf)

def handle_option_5(lf):
    print("Available PNR Numbers:")
    print(lf.index.tolist())
    try:
        pnr = int(input("Enter your PNR number: "))
        print(lf.loc[pnr])
    except KeyError:
        print("Invalid PNR number.")

def handle_option_6(lf):
    # Age group graph
    age_ranges = [f"{i}-{i+10}" for i in range(0, 100, 10)]
    lf['age_group'] = pd.cut(lf['age'], bins=range(0, 101, 10), labels=age_ranges, right=False)
    counts = lf['age_group'].value_counts().sort_index()
    plt.bar(counts.index, counts.values, color='skyblue')
    plt.title("Passenger Count by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Number of Passengers")
    plt.tight_layout()
    plt.show()

def handle_option_7(lf):
    print("\nStatistics about Passenger Fares")
    print("====================================")
    print(f"Mean Fare:    ₹{lf['fare'].mean():.2f}")
    print(f"Median Fare:  ₹{lf['fare'].median():.2f}")
    print(f"Min Fare:     ₹{lf['fare'].min():.2f}")
    print(f"Max Fare:     ₹{lf['fare'].max():.2f}")
    print("====================================")

def handle_option_8(df):
    try:
        train_number = int(input("Enter train number to search: "))
        result = df[df['train_no'] == train_number]
        if not result.empty:
            print("Train Found:")
            print(result)
        else:
            print("No train with that number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# ----------------------------- Main Program -----------------------------

def main():
    print("\n" + "#"*72)
    print(" " * 15 + ".....Welcome to Train Reservation System.....\n")

    credentials = load_user_credentials()

    while True:
        print("\n1) Register\n2) Login\n3) Quit")
        choice = input("Select an option: ")

        if choice == "1":
            register(credentials)
        elif choice == "2":
            if login(credentials):
                break
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid input.")

    while True:
        try:
            df = pd.read_csv(TRAIN_CSV, index_col="sno")
        except:
            df = pd.DataFrame(columns=["train_no", "train_name", "start", "end"])
        try:
            lf = pd.read_csv(RESERVATION_CSV, index_col="pnr_no")
        except:
            lf = pd.DataFrame(columns=["name", "age", "way_from", "way_to", "confirmation", "fare"])

        print("\n" + "+" * 70)
        print("1) Add Train Details")
        print("2) Remove Train Detail")
        print("3) New Reservation")
        print("4) Show All Reservation Details")
        print("5) Show Your Reservation Details")
        print("6) Show Graph - Age Group of Passengers")
        print("7) Analyze Fare Statistics")
        print("8) Search Train by Train Number")
        print("9) Logout")
        print("+" * 70)

        try:
            option = int(input("Select your option: "))
        except ValueError:
            print("Please enter a number between 1 and 9.")
            continue

        if option == 1:
            handle_option_1(df)
        elif option == 2:
            handle_option_2(df)
        elif option == 3:
            handle_option_3(lf)
        elif option == 4:
            handle_option_4(lf)
        elif option == 5:
            handle_option_5(lf)
        elif option == 6:
            handle_option_6(lf)
        elif option == 7:
            handle_option_7(lf)
        elif option == 8:
            handle_option_8(df)
        elif option == 9:
            print("Logging out...")
            break
        else:
            print("Invalid option.")

        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
