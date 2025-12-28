🍕 A La Carte
Order. Eat. Rate. Repeat.

A console-based food ordering & delivery application built using Python and MySQL, simulating how real-world food delivery platforms work.


What is A La Carte?

A La Carte is a menu-driven CLI application where:

🏪 Restaurants manage their menus & track orders

🧑‍🍳 Customers browse, order food & rate restaurants

📊 Orders & ratings are stored and managed using MySQL

Think of it as a mini Swiggy/Zomato, but in the terminal.
<br><br><br><br>
🎮 What Can You Do?

🔐 Login System

Separate login for Restaurant Owners & Customers

Username & password validation

Strong password rules

3-attempt login limit
<br><br>

MODE 1:
🏪 Restaurant Owner Mode

✏️ Add / Edit restaurant details

📋 Add & delete menu items

📦 View customer orders (sales)

⭐ View average ratings

<br><br>

MODE 2:
🧑‍🍳 Customer Mode

👤 Create & update profile

🍽️ Browse restaurants

📜 View menus

🛒 Order food with quantity selection

💳 Choose payment method (Card / COD / UPI)

🕒 View past orders

⭐ Rate restaurants
<br><br><br><br>

🗄️ Behind the Scenes (Database)

All data is stored in MySQL, including:

Users (restaurants & customers)

Menus

Orders

Ratings

📌 Tables are automatically created when the app runs for the first time.
<br><br><br><br>

🛠️ Tech Stack
Technology	Used For
🐍 Python	Application Logic
🗄️ MySQL	Database
⌨️ CLI	User Interface
🕒 datetime	Order timestamps
▶️ How to Run This Project

<br><br><br><br>

✅ Prerequisites

Python 3.x

MySQL Server running

📦 Install Required Package
pip install mysql-connector-python

🔧 Update Database Credentials

Edit this part in the code:

mycon = sqltor.connect(
    host="localhost",
    user="root",
    password="pass"
)

🚀 Run the App
python main.py

<br><br><br><br>

Sit back and enjoy ordering food from your terminal 😄
<br><br><br><br>

🧠 How the App Flows
App Start
   ↓
Choose User (Restaurant / Customer)
   ↓
Login or Create Account
   ↓
Role-based Menu
   ↓
Database Operations
   ↓
Exit
<br><br><br><br>

⚠️ Current Limitations

Console-based (no GUI / web UI)

Passwords stored as plain text

No real payment gateway

<br><br><br><br>

🚀<u>Enhancements(currently happening)</u>

🌐 Convert to Flask / Django web app ( already into it)
🔐 Password hashing
📦 Order status tracking
🧑‍💼 Admin panel
🎨 Frontend UI(doing)
🛡️ Secure SQL queries
<br><br><br><br>

👨‍💻 Author
Naman Chaddha
📘 Python-MySQL Project

⭐ Like this project?

Give it a ⭐ on GitHub — it really helps!
