<div align="center">

# 🚂 Railway Reservation System

**A Python-based command-line application for managing train bookings, passenger records, and travel analytics.**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 📌 Overview

The **Railway Reservation System** is a fully functional CLI application built in Python. It supports user registration and login with hashed password security, train management, seat reservations with auto-generated PNR numbers, and data analytics through matplotlib visualizations — all stored using lightweight CSV files, no database required.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Secure Auth** | Register & login with SHA-256 hashed passwords |
| 🚆 **Train Management** | Add and remove train records |
| 🎟️ **Book Reservation** | Auto-generates unique PNR number and fare |
| ❌ **Cancel Reservation** | Cancel any booking by PNR |
| 📋 **View All Bookings** | See every reservation in the system |
| 🔍 **PNR Lookup** | Fetch your booking details instantly |
| 📊 **Age Group Graph** | Colour-coded bar chart of passengers by age |
| 💰 **Fare Analytics** | Stats + histogram with mean/median lines |
| 🔎 **Train Search** | Find a train by its train number |

---

## 🗂️ Project Structure

```
Railway-Reservation-System/
│
├── main.py                  # Main application entry point
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignores credentials & cache files
├── README.md                # Project documentation
│
└── data/
    ├── trains.csv           # Train records
    ├── reservations.csv     # Passenger reservation records
    └── user_credentials.csv # Hashed user credentials (auto-created)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher 

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/BlAckCAt-SAGAR/Railway-Reservation-System.git
cd Railway-Reservation-System
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the application**
```bash
python main.py
```

> ⚠️ Always run from inside the project folder so the `data/` path resolves correctly.

---

## 🖥️ Usage

### Authentication Menu
```
  1) Register
  2) Login
  3) Quit
```

### Main Menu (after login)
```
+-------------------------------------------------------+
   RAILWAY RESERVATION SYSTEM — MAIN MENU
+-------------------------------------------------------+
  1)  Add Train Details
  2)  Remove Train Detail
  3)  New Reservation
  4)  Show All Reservations
  5)  Show My Reservation (by PNR)
  6)  Cancel a Reservation
  7)  Age Group Graph
  8)  Fare Statistics & Graph
  9)  Search Train by Number
  10) Logout
+-------------------------------------------------------+
```

### Sample Booking Output
```
=============================================
         BOOKING CONFIRMED
=============================================
  PNR Number   : 482910
  Passenger    : Aarav Sharma (Age: 24)
  From         : Mumbai
  To           : Pune
  Fare         : Rs. 850
  Status       : Confirmed
=============================================
```

### Sample Fare Statistics Output
```
==========================================
    PASSENGER FARE STATISTICS
==========================================
  Total Passengers : 30
  Mean Fare        : Rs. 1663.33
  Median Fare      : Rs. 1575.00
  Min Fare         : Rs.  550.00
  Max Fare         : Rs. 3400.00
  Std Deviation    : Rs.  745.21
  Total Revenue    : Rs. 49900.00
==========================================
```

---

## 🔐 Security

- Passwords are **never stored in plain text**
- Every password is hashed using **SHA-256** before saving to `user_credentials.csv`
- The credentials file is listed in `.gitignore` so it is never accidentally pushed to GitHub
- Minimum password length of **6 characters** is enforced at registration

---

## 📊 Analytics & Graphs

The system generates two types of visualizations:

**Age Group Bar Chart** — shows the distribution of passengers across age brackets (0–10, 10–20 ... 90–100) with value labels on each bar and a colour gradient from red to green.

**Fare Distribution Histogram** — shows how fares are spread across all bookings, with dashed lines marking the mean and median fare values.

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Data Handling:** Pandas, NumPy
- **Visualizations:** Matplotlib
- **Storage:** CSV flat files
- **Security:** hashlib (SHA-256)

---

## 📋 Requirements

```
pandas
numpy
matplotlib
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 👤 Author

**Sagar** — [@BlAckCAt-SAGAR](https://github.com/BlAckCAt-SAGAR)

---

## ⭐ Show Your Support

If you found this project helpful, please give it a **star** ⭐ on GitHub — it really helps!

---

<div align="center">
Made with ❤️ and Python
</div>
