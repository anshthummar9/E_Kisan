# E_Kisan (Smart Agriculture System)

E_Kisan is an AI-powered agriculture web application built with Django. It assists farmers and agricultural enthusiasts by analyzing soil and weather data to provide Machine Learning-based recommendations for the most suitable crops to grow and the required fertilizers.

## 🌟 Key Features

- **User Authentication:** Secure registration, login, and logout functionalities.
- **Soil Analysis & Crop Prediction:** Takes soil parameters (N, P, K levels, pH, soil color) and suggests the best crop using a trained Machine Learning model.
- **Fertilizer Recommendation:** Predicts the appropriate fertilizer based on the soil data, predicted crop, and environmental factors.
- **Weather Integration:** Automatically fetches real-time temperature and rainfall data for the user's city using the OpenWeatherMap API to improve prediction accuracy.
- **User Dashboard:** Maintains a history of soil reports and provides visual charts tracking Nitrogen, Phosphorus, and Potassium (N-P-K) levels over time.

## 🛠️ Tech Stack

- **Backend:** 
  - Python 3.x
  - Django 6.0.2 (Web Framework)
  - requests (API Integration)
  - python-dotenv (Environment Variable Management)
- **Machine Learning & Data Processing:** 
  - scikit-learn (Model Training & Inference)
  - Pandas (Data Manipulation)
  - NumPy (Numerical Computations)
  - Joblib (Model Serialization)
- **Database:** 
  - MySQL via `mysqlclient` 
- **Frontend:** 
  - HTML5, CSS3, JavaScript
  - Django Templates (Server-side rendering)
  - Bootstrap 5.3.0 (CSS Framework for Styling and Responsive Layout)
  - Chart.js (Data Visualization for N-P-K graphs)
- **External APIs & Services:** 
  - OpenWeatherMap API (Real-time weather data integration)

## ⚙️ Prerequisites

- Python 3.x installed on your system
- MySQL Server 5.7+ installed and running
- An API key from [OpenWeatherMap](https://openweathermap.org/api)

## 🗄️ Database Setup

This project uses **MySQL** as its database backend via the `mysqlclient` Python package.

### 1. Install MySQL

Download and install [MySQL Community Server](https://dev.mysql.com/downloads/mysql/). During setup, note the root password you configure — you'll need it below.

### 2. Configure Database Environment Variables

Add the following variables to your `.env` file in the project root (alongside `manage.py`):

```env
DB_NAME=EKisan_db
DB_USER=root
DB_PASSWORD=your_mysql_root_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

| Variable      | Default      | Description                        |
|---------------|--------------|------------------------------------|
| `DB_NAME`     | `EKisan_db`  | Name of the MySQL database         |
| `DB_USER`     | `root`       | MySQL username                     |
| `DB_PASSWORD` | `password`   | MySQL user password                |
| `DB_HOST`     | `127.0.0.1`  | MySQL host address                 |
| `DB_PORT`     | `3306`       | MySQL port                         |

### 3. Create the Database

A helper script is provided to automatically create the database if it doesn't already exist. Run it from the project root:

```bash
python scripts/create_db.py
```

This script connects to MySQL using your `.env` credentials and runs:

```sql
CREATE DATABASE IF NOT EXISTS EKisan_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

> **Note:** If you prefer to create the database manually, open a MySQL shell and run the SQL command above.

### 4. Apply Django Migrations

After the database is created, apply Django's migrations to set up all tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🚀 Installation & Setup Instructions

Follow these steps to set up the project locally:

1. **Navigate to the project directory:**

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Environment Variables:**
   A `.env` file may already exist, or you can create one in the root directory (where `manage.py` is located) and add your OpenWeatherMap API key:
   ```env
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   ```

6. **Apply Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **(Optional) Create a Superuser** for the Django admin panel:
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## 📁 Project Structure

```text
E_Kisan/
├── EKisan/             # Main Django project settings & URL configurations
├── accounts/           # App handling user authentication & registration
├── analysis/           # Core app for soil analysis predictions
│   ├── ml_models/      # Pre-trained ML models (crop & fertilizer .pkl files)
│   ├── migrations/     # Database migration history
│   ├── utils.py        # Utility functions (e.g., OpenWeatherMap API wrapper)
│   ├── views.py        # Business logic for form processing and dashboard
│   └── models.py       # Databse schema for SoilReport history
├── static/             # CSS, JS, and image assets
├── templates/          # Global HTML templates (base.html, dashboard view)
├── manage.py           # Django's command-line utility for administrative tasks
├── requirements.txt    # List of required Python packages
└── .env                # Environment variables (API keys, DB config)
```

## 📝 Usage

1. **Register/Login** to the application.
2. Go to the **Soil Analysis** page.
3. Enter your soil details (Nitrogen, Phosphorus, Potassium, pH, Soil Color) and your City.
4. Submit the form to view the prediction report for the best-suited crop and the required fertilizer.
5. Track your history and view graphical trends of soil nutrients from your personal **Dashboard**.
