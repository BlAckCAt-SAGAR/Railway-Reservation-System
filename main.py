import csv
import hashlib
import os
import random
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── File Paths (relative, works on any machine) ───────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
DATA_DIR        = os.path.join(BASE_DIR, "data")
TRAIN_CSV       = os.path.join(DATA_DIR, "trains.csv")
RESERVATION_CSV = os.path.join(DATA_DIR, "reservations.csv")
CREDENTIALS_CSV = os.path.join(DATA_DIR, "user_credentials.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# ── Password Hashing ──────────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    """SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()

# ── Credential Helpers ────────────────────────────────────────────────────────
def load_credentials() -> dict:
    credentials = {}
    try:
        with open(CREDENTIALS_CSV, mode="r") as f:
            for row in csv.reader(f):
                if len(row) == 2:
                    credentials[row[0]] = row[1]
    except FileNotFoundError:
        pass
    return credentials

def save_credentials(credentials: dict) -> None:
    with open(CREDENTIALS_CSV, mode="w", newline="") as f:
        writer = csv.writer(f)
        for username, pwd_hash in credentials.items():
            writer.writerow([username, pwd_hash])

# ── Auth ──────────────────────────────────────────────────────────────────────
def register(credentials: dict) -> None:
    print("\n--- Register ---")
    username = input("Choose a username : ").strip()
    if not username:
        print("[!] Username cannot be empty.")
        return
    if username in credentials:
        print("[!] Username already exists. Please choose another.")
        return

    password = input("Choose a password : ").strip()
    if len(password) < 6:
        print("[!] Password must be at least 6 characters.")
        return

    confirm = input("Confirm password  : ").strip()
    if password != confirm:
        print("[!] Passwords do not match.")
        return

    credentials[username] = hash_password(password)
    save_credentials(credentials)
    print("[✓] Registration successful!")

def login(credentials: dict) -> bool:
    print("\n--- Login ---")
    username = input("Username : ").strip()
    password = input("Password : ").strip()
    stored = credentials.get(username)
    if stored and stored == hash_password(password):
        print(f"[✓] Welcome back, {username}!")
        return True
    print("[!] Invalid username or password.")
    return False

# ── CSV Load Helpers ──────────────────────────────────────────────────────────
def load_trains() -> pd.DataFrame:
    try:
        df = pd.read_csv(TRAIN_CSV, index_col="sno")
        df.index = df.index.astype(int)
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=["train_no", "train_name", "start", "end"])

def load_reservations() -> pd.DataFrame:
    try:
        lf = pd.read_csv(RESERVATION_CSV, index_col="pnr_no")
        lf.index = lf.index.astype(int)
        return lf
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=["name", "age", "way_from", "way_to", "confirmed", "fare"])

# ── Menu Option Handlers ──────────────────────────────────────────────────────
def handle_add_train(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- Add Train ---")
    print(df.to_string() if not df.empty else "(No trains yet)")

    try:
        sno      = int(input("\nSerial No      : "))
        train_no = int(input("Train Number   : "))
    except ValueError:
        print("[!] Serial No and Train Number must be integers.")
        return df

    train_name = input("Train Name     : ").strip()
    start      = input("Start Station  : ").strip()
    end        = input("End Station    : ").strip()

    if not train_name or not start or not end:
        print("[!] Fields cannot be empty.")
        return df

    df.loc[sno] = [train_no, train_name, start, end]
    df.to_csv(TRAIN_CSV, index_label="sno")
    print("[✓] Train added successfully!")
    return df

def handle_remove_train(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- Remove Train ---")
    if df.empty:
        print("[!] No trains to remove.")
        return df

    print(df.to_string())
    try:
        sno = int(input("\nEnter Serial No to remove: "))
    except ValueError:
        print("[!] Please enter a valid integer.")
        return df

    if sno in df.index:
        df.drop(sno, inplace=True)
        df.to_csv(TRAIN_CSV, index_label="sno")
        print("[✓] Train removed successfully.")
    else:
        print("[!] Serial No not found.")
    return df

def handle_new_reservation(lf: pd.DataFrame) -> pd.DataFrame:
    print("\n--- New Reservation ---")
    name = input("Passenger Name  : ").strip()
    if not name:
        print("[!] Name cannot be empty.")
        return lf

    try:
        age = int(input("Age             : "))
        if not (1 <= age <= 120):
            raise ValueError
    except ValueError:
        print("[!] Please enter a valid age (1-120).")
        return lf

    way_from = input("From Station    : ").strip()
    way_to   = input("To Station      : ").strip()
    if not way_from or not way_to:
        print("[!] Station names cannot be empty.")
        return lf

    # Generate unique PNR
    existing_pnrs = set(lf.index.tolist())
    pnr_no = random.randint(100000, 999999)
    while pnr_no in existing_pnrs:
        pnr_no = random.randint(100000, 999999)

    fare = random.randint(500, 3500)
    lf.loc[pnr_no] = [name, age, way_from, way_to, "Confirmed", fare]
    lf.to_csv(RESERVATION_CSV, index_label="pnr_no")

    print("\n" + "=" * 45)
    print("         BOOKING CONFIRMED")
    print("=" * 45)
    print(f"  PNR Number   : {pnr_no}")
    print(f"  Passenger    : {name} (Age: {age})")
    print(f"  From         : {way_from}")
    print(f"  To           : {way_to}")
    print(f"  Fare         : Rs. {fare}")
    print(f"  Status       : Confirmed")
    print("=" * 45)
    return lf

def handle_show_all_reservations(lf: pd.DataFrame) -> None:
    print("\n--- All Reservations ---")
    if lf.empty:
        print("[!] No reservations found.")
        return
    print(lf.to_string())

def handle_show_my_reservation(lf: pd.DataFrame) -> None:
    print("\n--- My Reservation ---")
    if lf.empty:
        print("[!] No reservations found.")
        return

    print("Available PNR Numbers:", lf.index.tolist())
    try:
        pnr = int(input("Enter your PNR number: "))
        row = lf.loc[pnr]
        print("\n" + "=" * 40)
        print(f"  PNR       : {pnr}")
        print(f"  Name      : {row['name']}")
        print(f"  Age       : {row['age']}")
        print(f"  From      : {row['way_from']}")
        print(f"  To        : {row['way_to']}")
        print(f"  Status    : {row['confirmed']}")
        print(f"  Fare      : Rs. {row['fare']}")
        print("=" * 40)
    except (KeyError, ValueError):
        print("[!] PNR number not found.")

def handle_cancel_reservation(lf: pd.DataFrame) -> pd.DataFrame:
    print("\n--- Cancel Reservation ---")
    if lf.empty:
        print("[!] No reservations to cancel.")
        return lf

    print("Your PNR Numbers:", lf.index.tolist())
    try:
        pnr = int(input("Enter PNR to cancel: "))
    except ValueError:
        print("[!] Invalid PNR.")
        return lf

    if pnr in lf.index:
        passenger = lf.loc[pnr, "name"]
        lf.drop(pnr, inplace=True)
        lf.to_csv(RESERVATION_CSV, index_label="pnr_no")
        print(f"[✓] Reservation for {passenger} (PNR: {pnr}) cancelled.")
    else:
        print("[!] PNR not found.")
    return lf

def handle_age_graph(lf: pd.DataFrame) -> None:
    print("\n--- Age Group Graph ---")
    if lf.empty:
        print("[!] No reservation data to plot.")
        return

    age_ranges = [f"{i}-{i+10}" for i in range(0, 100, 10)]
    lf["age_group"] = pd.cut(
        lf["age"].astype(int),
        bins=list(range(0, 101, 10)),          # 11 edges → 10 buckets
        labels=[f"{i}-{i+10}" for i in range(0, 100, 10)],  # 10 labels
        right=False
    )
    counts = lf["age_group"].value_counts().sort_index()

    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.9, len(counts)))
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(counts.index, counts.values, color=colors, edgecolor="white", linewidth=1.2)

    # Value labels on bars
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.annotate(
                f"{int(height)}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha="center", va="bottom", fontsize=10, fontweight="bold"
            )

    ax.set_title("Passengers by Age Group", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Age Group", fontsize=13)
    ax.set_ylabel("Number of Passengers", fontsize=13)
    ax.set_ylim(0, counts.max() + 3)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()

def handle_fare_stats(lf: pd.DataFrame) -> None:
    print("\n--- Fare Statistics ---")
    if lf.empty:
        print("[!] No reservation data available.")
        return

    fares = lf["fare"].astype(float)
    print("\n" + "=" * 42)
    print("    PASSENGER FARE STATISTICS")
    print("=" * 42)
    print(f"  Total Passengers : {len(fares)}")
    print(f"  Mean Fare        : Rs. {fares.mean():.2f}")
    print(f"  Median Fare      : Rs. {fares.median():.2f}")
    print(f"  Min Fare         : Rs. {fares.min():.2f}")
    print(f"  Max Fare         : Rs. {fares.max():.2f}")
    print(f"  Std Deviation    : Rs. {fares.std():.2f}")
    print(f"  Total Revenue    : Rs. {fares.sum():.2f}")
    print("=" * 42)

    # Fare distribution graph
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(fares, bins=10, color="#4C9BE8", edgecolor="white", linewidth=1.2)
    ax.axvline(fares.mean(), color="red", linestyle="--", linewidth=1.5, label=f"Mean: Rs.{fares.mean():.0f}")
    ax.axvline(fares.median(), color="green", linestyle="--", linewidth=1.5, label=f"Median: Rs.{fares.median():.0f}")
    ax.set_title("Fare Distribution of Passengers", fontsize=15, fontweight="bold")
    ax.set_xlabel("Fare (Rs.)", fontsize=12)
    ax.set_ylabel("Number of Passengers", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.show()

def handle_search_train(df: pd.DataFrame) -> None:
    print("\n--- Search Train ---")
    if df.empty:
        print("[!] No train records available.")
        return

    try:
        train_number = int(input("Enter Train Number to search: "))
    except ValueError:
        print("[!] Please enter a valid number.")
        return

    result = df[df["train_no"] == train_number]
    if not result.empty:
        print("\n[✓] Train Found:")
        print(result.to_string())
    else:
        print(f"[!] No train found with number {train_number}.")

# ── Main Program ──────────────────────────────────────────────────────────────
def show_menu() -> None:
    print("\n" + "+" * 55)
    print("   RAILWAY RESERVATION SYSTEM — MAIN MENU")
    print("+" * 55)
    print("  1)  Add Train Details")
    print("  2)  Remove Train Detail")
    print("  3)  New Reservation")
    print("  4)  Show All Reservations")
    print("  5)  Show My Reservation (by PNR)")
    print("  6)  Cancel a Reservation")
    print("  7)  Age Group Graph")
    print("  8)  Fare Statistics & Graph")
    print("  9)  Search Train by Number")
    print("  10) Logout")
    print("+" * 55)

def main():
    print("\n" + "#" * 55)
    print("   Welcome to the Railway Reservation System")
    print("#" * 55)

    credentials = load_credentials()

    # ── Auth Loop ──
    while True:
        print("\n  1) Register")
        print("  2) Login")
        print("  3) Quit")
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            register(credentials)
        elif choice == "2":
            if login(credentials):
                break
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("[!] Invalid choice.")

    # ── Main Menu Loop ──
    while True:
        df = load_trains()
        lf = load_reservations()

        show_menu()

        try:
            option = int(input("Select your option: ").strip())
        except ValueError:
            print("[!] Please enter a number.")
            input("Press Enter to continue...")
            continue

        if   option == 1:  df = handle_add_train(df)
        elif option == 2:  df = handle_remove_train(df)
        elif option == 3:  lf = handle_new_reservation(lf)
        elif option == 4:  handle_show_all_reservations(lf)
        elif option == 5:  handle_show_my_reservation(lf)
        elif option == 6:  lf = handle_cancel_reservation(lf)
        elif option == 7:  handle_age_graph(lf)
        elif option == 8:  handle_fare_stats(lf)
        elif option == 9:  handle_search_train(df)
        elif option == 10:
            print("[✓] Logged out successfully.")
            main()   # loop back to login screen
            return
        else:
            print("[!] Invalid option. Choose between 1 and 10.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
