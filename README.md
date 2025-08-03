# Smart Irrigation System for Efficient Agriculture 💧

This repository contains the code and resources for a **Smart Irrigation System** designed to optimize water usage in farming. The project leverages machine learning to predict the optimal sprinkler status for different farm parcels based on real-time sensor data, aiming to reduce water wastage and enhance agricultural efficiency.

---

## 🚀 Project Overview

In an era of increasing water scarcity, efficient irrigation is paramount. This project addresses the challenge by building an intelligent system that automates irrigation decisions. It uses sensor data to predict when and where water is needed, moving beyond traditional, often wasteful, manual methods.

### Learning Objectives Achieved:
* Gained practical experience in **data preprocessing** and **Exploratory Data Analysis (EDA)**.
* Developed and trained a **multi-output classification model** using `scikit-learn`.
* Understood model evaluation techniques for multi-label classification.
* Deployed a machine learning model into an interactive web application using **Streamlit**.

---

## ✨ Features

* **Sensor Data Processing**: Handles and preprocesses sensor readings from a farm.
* **Intelligent Prediction**: Predicts the ON/OFF status for three distinct farm parcels.
* **Machine Learning Model**: Utilizes a `RandomForestClassifier` wrapped in a `MultiOutputClassifier` for robust predictions.
* **Interactive Web Application**: A user-friendly Streamlit interface for real-time predictions based on user-input sensor values.
* **Model Persistence**: Saves the trained model for easy deployment and reuse.

---

## 📊 Dataset

The project uses the `irrigation_machine.csv` dataset, which contains:
* `sensor_0` to `sensor_19`: 20 features representing various sensor readings.
* `parcel_0`, `parcel_1`, `parcel_2`: Three target labels indicating the ON/OFF status (0 or 1) for each sprinkler parcel.

---

## 🛠️ Technologies Used

* **Python 🐍**: The primary programming language.
* **Pandas**: For data manipulation and analysis.
* **NumPy**: For numerical operations.
* **Scikit-learn**: For machine learning (model training, preprocessing, evaluation).
* **Matplotlib & Seaborn**: For data visualization.
* **Joblib**: For saving and loading Python objects (the trained model).
* **Streamlit**: For creating the interactive web application.
* **Google Colab**: Used for model training and `.pkl` file generation.
* **Git & GitHub**: For version control and repository hosting.

---

## ⚙️ Setup and Local Execution

Follow these steps to set up and run the Smart Irrigation System on your local machine:

### Step 1: Google Colab - Train Model & Generate `.pkl`

1.  **Open the Colab Notebook**: Go to [Smart_Irrigation_System_Notebook.ipynb](https://colab.research.google.com/github/RGS-AI/AICTE_Internships/blob/main/2025/July_2025/Smart_Irrigation/Irrigation_System%20(3).ipynb) (or upload your local `.ipynb` file to Colab).
2.  **Upload `irrigation_machine.csv`**: In the Colab notebook, run the cell containing `from google.colab import files; uploaded = files.upload()`. Select and upload your `irrigation_machine.csv` file.
3.  **Run All Cells**: Execute all cells in the Colab notebook sequentially. This will perform data preprocessing, model training, evaluation, and save the trained model as `Farm_Irrigation_System.pkl`.
4.  **Download `Farm_Irrigation_System.pkl`**: After execution, download the `Farm_Irrigation_System.pkl` file from your Colab environment to your local machine.

### Step 2: Local Machine - Set up Streamlit App

1.  **Create Project Directory**: Ensure you have a dedicated folder for your project (e.g., `/home/prak05/Streamlit`).
2.  **Place Files**: Put the downloaded `Farm_Irrigation_System.pkl` file and your `streamlit.py` (your Streamlit app code) file into this directory.
3.  **Open Terminal**: Navigate to your project directory in the terminal:
    ```bash
    cd /home/prak05/Streamlit
    ```
4.  **Create & Activate Virtual Environment**: (Highly Recommended for Kali Linux)
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate
    ```
    Your terminal prompt should change to `(myenv)┌──(prak05㉿pecadosdeprak)-[~/Streamlit]`.
5.  **Install Dependencies**: With the virtual environment activated, install all required Python packages:
    ```bash
    pip install streamlit numpy joblib scikit-learn
    ```
6.  **Run Streamlit App**: Execute your Streamlit application:
    ```bash
    streamlit run streamlit.py
    ```
    This command will launch the Streamlit app in your default web browser (usually at `http://localhost:8501`).

---

## 📂 Repository Structure

.
├── Farm_Irrigation_System.pkl  # Trained machine learning model
├── irrigation_machine.csv      # Dataset used for training
├── Irrigation_System (3).ipynb # Google Colab Notebook (model training & evaluation)
├── streamlit.py                # Streamlit web application code
└── README.md                   # This README file
