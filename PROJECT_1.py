import csv
import pandas as pd
import numpy as np
import sys
import random
import matplotlib.pyplot as plt

# User credentials dictionary
user_credentials = {}

# Load user data from a CSV file
def load_user_credentials():
    user_credentials = {}
    try:
        with open("user_credentials.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                username, password = row
                user_credentials[username] = password
    except FileNotFoundError:
        pass
    return user_credentials

# Function to save user data to a CSV file
def save_user_credentials(user_credentials):
    with open("user_credentials.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        for username, password in user_credentials.items():
            writer.writerow([username, password])

# Load user data from CSV file
user_credentials = load_user_credentials()

def register(username, password):
    if username in user_credentials:
        print("Username already exists. Please choose a different one.")
    else:
        user_credentials[username] = password
        save_user_credentials(user_credentials)
        print("Registration successful!")

def login(username, password):
    if username in user_credentials and user_credentials[username] == password:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False
print()
print()
print('########################################################################')
print()
print()
print(' ' * 70, ".....Welcome to Train Reservation.....",)
print()
print()

while True:
    logged_in = False  # Flag to track if the user is logged in

    while not logged_in:
        print("\n1) Register\n2) Login\n3) Quit")
        choice = input("Select an option: ")

        if choice == "1":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            register(username, password)

        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if login(username, password):
                logged_in = True  # Set the flag to True after successful login

        elif choice == "3":
            print("Goodbye!")
            sys.exit()
            sys

        else:
            print("Invalid choice. Please try again.")

    # The user is now logged in, so they can access the reservation system

    df = pd.read_csv("D:\c\csv2.csv", index_col="sno")
    lf = pd.read_csv("D:\c\csv1.csv", index_col="pnr_no")

    # Rest of your code for managing train reservations, etc.

    a=print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    b=print("+        1) Add Train Details                                                                                                                                                +")
    print("+        2) Remove Train Detail                                                                                                                                             +")
    print("+        3) New Reservation                                                                                                                                                   +")
    print("+        4) Show All Reservation Details                                                                                                                                +")
    print("+        5) Show our Reservation Details                                                                                                                               +")
    print("+        6) Show graph for fare of passengers                                                                                                                        +")
    print("+        7) Analyze and display statistics about passenger fares                                                                                             +")
    print("+        8) Search for a train by its train number                                                                                                                    +")
    print("+        9) Logout                                                                                                                                                                   +")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    option = int(input("Select your option: "))

    if option == 1:
        
        # ... (rest of your code for adding train details)
        print()
        print()
        print(pd.read_csv("D:\c\csv2.csv"))
        print()
        sno = int(input("Enter s.no: "))
        print()
        train_no = int(input("Enter train no.: "))
        print()
        train_name = input("Enter train name: ")
        print()
        start = input("Enter train start station: ")
        print()
        end = input("Enter train end station: ")
        print()
        df.loc[sno, :] = [train_no, train_name, start, end]
        df.to_csv("D:\c\csv2.csv")
        print(' ' * 10, "processing...")
        print()
        print()
        
    elif option == 2:
        # ... (rest of your code for removing train details)
        print()
        print(df)
        print()
        sno = int(input("Enter s.no to be removed : "))
        print()
        df.drop(sno, axis=0, inplace=True)
        df.to_csv("D:\c\csv2.csv")
        print('Processing...')
        print()
        print()
        print(df)
        print()
        print()
        print()
        
    elif option == 3:
        # ... (rest of your code for new reservation)
        print()
        NAME = input("Enter your name: ")
        print()
        AGE = int(input("Enter your age: "))
        print()
        WAY_FROM = input("Enter way from station: ")
        print()
        WAY_TO = input("Enter way to station: ")
        print()
        pnr_no = random.randint(111111, 999999)
        FARE= random.randint(1000, 3500)
        CONFIRMATION = 'y'
        lf.loc[pnr_no, :] = [NAME, AGE, WAY_FROM, WAY_TO, CONFIRMATION, FARE]
        lf.to_csv("D:\c\csv1.csv")
        print('Processing...')
        print()
        print()
        print("Your PNR_NO :",pnr_no)
        print()
        print()
        print()
        print('Reservation Successful')
        print("#######################################################################")
        
        
    elif option == 4:
        # ... (rest of your code for showing all reservation details)
        print()
        print(lf)
        print()
        print()
        
    elif option == 5:
        # ... (rest of your code for showing reservation details)
        print(' ' * 10, '*** |__| PNR_NO |__| ***')
        print()
        print(pd.Series(lf.index))
        print()
        print()
        pnr_no = int(input("Enter your pnr_no.: "))
        print()
        detail = lf.loc[pnr_no, :]
        print()
        print(' ' * 10, 'Details related with this', pnr_no, 'is...')
        print()
        print()
        print(detail)
        print()
        print()
        
        
    elif option == 6:
        # ... (rest of your code for showing graph)
        df_CSV1=pd.read_csv("D:\c\csv1.csv")
        plt.figure(figsize=(9,6))
        plt.bar(x=df_CSV1['name'],
        height=df_CSV1['fare'],color='red')
        plt.title('Fare of passengers')
        plt.savefig('Fare of passengers.png.')
        plt.show()
        
        
    elif option == 7:
    # Analyze and display statistics about passenger fares
        df_CSV1=pd.read_csv("D:\c\csv1.csv")
        print()
        print("Statistics about Passenger Fares:")
        print("                      ====================================")
        print("                     |    Mean Fare:", df_CSV1['fare'].mean()     )
        print("                     |    Median Fare:", df_CSV1['fare'].median() )
        print("                     |    Minimum Fare:", df_CSV1['fare'].min()   )
        print("                     |    Maximum Fare:", df_CSV1['fare'].max()   )
        print("                      ====================================")
        
        
    
    elif option == 8:
    # Search for a train by its train number
        print(df)
        train_number = int(input("Enter the train number: "))
        train_info = df[df['train_no'] == train_number]
    
        if not train_info.empty:
            print("Train Information:")
            print(train_info)
        else:
            print("Train with train number {} not found.".format(train_number))
            

    elif option == 9:
        print("Logging out...")
        

    
        break
