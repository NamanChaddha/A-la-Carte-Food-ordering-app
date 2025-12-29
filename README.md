# A La Carte 
<img width="548" height="443" alt="image" src="https://github.com/user-attachments/assets/7001d758-aea8-4a33-8d60-f42f64b29e62" />

> **Order. Eat. Rate. Repeat.** A professional terminal-based food ordering and delivery ecosystem.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
---

## 📖 Overview
**A La Carte** is a robust console-based food ordering system built using **Python** and **MySQL**. It simulates the core logic of modern delivery platforms, handling everything from inventory management for restaurants to secure checkout flows for customers.

### Why this project?
- 🛠️ **Full CRUD Logic:** Create, Read, Update, and Delete data from a live SQL database.
- 🔐 **Secure Access:** Role-based authentication (Restaurant vs. Customer).
- 📊 **Relational Data:** Complex database design linking users, menus, and orders.

---

## 🎮 Key Features

<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <h3>🏪 Restaurant Management</h3>
      <ul>
        <li><b>Inventory Control:</b> Seamlessly add, update, or remove menu items.</li>
        <li><b>Order Tracking:</b> View incoming customer orders in real-time.</li>
        <li><b>Feedback Loop:</b> Monitor restaurant ratings and customer reviews.</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>🧑‍💻 Customer Experience</h3>
      <ul>
        <li><b>Smart Browsing:</b> Explore restaurants and dynamic menus.</li>
        <li><b>Cart System:</b> Select quantities and manage your meal.</li>
        <li><b>Secure Checkout:</b> Integrated flow for UPI, Card, or COD.</li>
        <li><b>History:</b> Track and rate past dining experiences.</li>
      </ul>
    </td>
  </tr>
</table>

---

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.x |
| **Database** | MySQL |
| **Connector** | `mysql-connector-python` |
| **Interface** | Command Line (CLI) |

---

## ▶️ Getting Started

### 1. Prerequisites
Ensure you have MySQL installed and running on your local machine.

### 2. Install Dependencies

pip install mysql-connector-python

3. Database Configuration
Open the main script and update your local MySQL credentials:

Python

mycon = sqltor.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD_HERE"
)
4. Run the Application
Bash

python main.py
Note: The system will automatically generate the required tables upon the first successful run.

<h3>Learning Outcomes</h3><br>
Database Design: Normalization and relationship mapping in MySQL.

Backend Logic: Handling state and session logic in a CLI environment.

Error Handling: Managing SQL exceptions and invalid user inputs.

<h3>Roadmap</h3><br>
-Security: Implement SHA-256 password hashing.

[ ] GUI: Transition from CLI to a web interface using Flask.

[ ] Admin Panel: A master dashboard for platform-wide analytics.

<p align="center"> Made with ❤️ by Naman Chaddha


<i>Give this project a ⭐ if you found it helpful!</i> </p>
