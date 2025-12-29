# 🍕 A La Carte 
> **Order. Eat. Rate. Repeat.** A professional terminal-based food ordering and delivery ecosystem.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

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
```bash
pip install mysql-connector-python
