# SQL Interface Web App

A deploy-ready Flask application designed for interacting with SQL databases through a clean web interface. It supports both **SQLite** (via file upload) and **MySQL** (via host/user/password input), displaying query results in a responsive, dark-themed layout.

## Features

* Upload and run queries on `.db` (SQLite) files
* Connect to MySQL with host, user, and password
* Execute `SELECT`, `INSERT`, `UPDATE`, `DELETE`, and other SQL commands
* View query results in styled, interactive tables
* Robust error handling and user feedback
* Dark theme, mobile-responsive UI for optimal viewing
* Session-based database tracking for a seamless user experience
* Toggleable MySQL setup instructions

---

## Folder Structure
```
sql-interface/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── databases/ # Directory for uploaded .db files
├── requirements.txt
└── Procfile
```
---

## Setup Locally

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/Sahilpal3/sql-interface.git](https://github.com/Sahilpal3/sql-interface.git)
    cd sql-interface
    ```
2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Application**
    ```bash
    python app.py
    ```
    Then, open your web browser and navigate to `http://localhost:5000`.
