# Iris Data Management System

A comprehensive web application for managing iris flower data and predicting species using Machine Learning.

## 📋 Overview

This project is a Django-based web application designed to collect, manage, and analyze Iris flower datasets. It integrates Scikit-learn to provide real-time species prediction using multiple machine learning algorithms.

## ✨ Features

### 🧠 AI & Machine Learning
- **Real-time Prediction:** Predict Iris species (Setosa, Versicolor, Virginica) based on sepal and petal measurements.
- **Multiple Algorithms:** Choose between:
  - K-Nearest Neighbors (KNN)
  - Decision Tree
  - Support Vector Machine (SVM)
- **Visual Feedback:** Displays the predicted species with an image.

### 📊 Data Management
- **CRUD Operations:** Create, Read, Update, and Delete iris records.
- **Search & Filtering:** Filter data by species name or minimum measurement values.
- **Import/Export:**
  - Bulk import data via CSV files.
  - Export current database to CSV.

### 🔐 User System
- **Authentication:** Secure Login and Registration.
- **Role-based Access:** Users are assigned roles (e.g., 'Reader') granting specific permissions.
- **Password Recovery:** Integrated password reset functionality via email.

### 🌐 User Interface
- **Modern UI:** Clean, responsive design with a professional look.
- **English Language:** Fully localized interface for international use.
- **Interactive Elements:** Dynamic tables, forms, and navigation.

## 🛠️ Technology Stack

- **Backend:** Python 3.x, Django 5.x
- **Data Analysis / ML:** Scikit-learn, NumPy, Pandas
- **Frontend:** HTML5, CSS3 (Custom styling)
- **Database:** SQLite (Default)
- **API:** Django Rest Framework

## 🚀 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/alidumn2/iris-data-management-system.git
    cd iris-data-management-system
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser (Optional)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

7.  **Access the App**
    Open your browser and navigate to `http://127.0.0.1:8000/`.

## 📂 Project Structure

- `iris_classifier/`: Main app directory containing views, models, and logic.
- `templates/`: HTML templates for the UI.
- `static/`: CSS styles and images.
- `iris_project/`: Project configuration and URL routing.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements.
