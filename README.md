# ⚡ Energy Save System

<p align="center">
  <img src="https://img.shields.io/badge/AI%20%26%20Data%20Science-Energy%20Management-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-Flask-green?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge" />
</p>

<p align="center">
  <b>Smart Energy Monitoring, Analysis & Alert System</b>
</p>

---

## 🌱 About the Project

**Energy Save System** is a web-based application developed to monitor and analyze household electricity consumption.

The system allows users to enter their energy usage for:

☀️ **Morning**
🌤️ **Afternoon**
🌙 **Night**

It calculates energy consumption, identifies the **peak usage period**, estimates the electricity cost, displays visual charts, provides smart energy-saving suggestions, and can send email alerts when the selected energy limit is exceeded.

---

## 🎯 Objectives

* ⚡ Monitor household electricity consumption
* 📊 Analyze energy usage by time period
* 🔍 Identify peak energy consumption hours
* 💰 Estimate electricity cost
* 🚨 Provide alerts when energy usage crosses a limit
* 💡 Suggest ways to reduce unnecessary energy consumption
* 📧 Send energy reports through email
* 🌍 Encourage energy conservation and responsible electricity usage

---

## ✨ Key Features

### 🏠 1. Home Page

A simple and interactive landing page that introduces the Energy Save System.

### 📝 2. Energy Input

Users can enter appliance power consumption and usage hours for:

* Morning
* Afternoon
* Night

The system calculates energy consumption in units.

### 📊 3. Energy Analysis Dashboard

The dashboard displays:

* ⚡ Total energy consumption
* 📈 Peak usage period
* 💰 Estimated electricity cost
* 📉 Line chart
* 🥧 Pie chart

### 🚨 4. Smart Alert System

Users can set an energy usage limit.

If the total usage exceeds the selected limit, the system identifies it as:

**⚠️ ENERGY LIMIT EXCEEDED**

Otherwise:

**✅ SAFE ENERGY USAGE**

### 📧 5. Email Reports

The application can send energy usage reports through Gmail.

The email report contains:

* Total energy usage
* Energy limit
* Peak usage period
* Usage status
* Smart suggestions
* Link to view the energy dashboard

### 💡 6. Energy Saving Tips

The system provides suggestions based on the detected peak usage period.

Examples include:

* Reduce unnecessary AC usage
* Turn off unused lights
* Avoid using multiple high-power appliances together
* Use LED bulbs
* Reduce unnecessary device usage

---

## 🌐 Ngrok Integration

**ngrok** was used during development and demonstration to expose the locally running Flask application through a temporary public URL.

This was useful for:

* 📱 Accessing the project from another device
* 📧 Providing a dashboard link in email reports
* 🧪 Testing the web application outside the local machine

> **Note:** The ngrok URL used during development is temporary and may change whenever a new ngrok session is started.

---

## 🛠️ Technologies Used

| Technology       | Purpose                          |
| ---------------- | -------------------------------- |
| 🐍 Python        | Backend programming              |
| 🌐 Flask         | Web application framework        |
| 📊 Chart.js      | Data visualization               |
| 🎨 HTML & CSS    | User interface                   |
| ⚙️ JavaScript    | Frontend interaction             |
| 📧 SMTP / Gmail  | Email notifications              |
| 🌐 ngrok         | Public access during development |
| 🔐 python-dotenv | Environment variable management  |

---

## 📂 Project Structure

```text
Energy-Save-System/
│
├── static/
│   ├── logo.png
│   └── header.png
│
├── app.py
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Energy-Save-System.git
```

### 2. Open the Project

```bash
cd Energy-Save-System
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

Create a `.env` file in the project folder:

```text
SENDER_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
SECRET_KEY=your-secret-key
```

⚠️ **Never upload `.env` to GitHub.**

The `.gitignore` file is used to prevent sensitive information from being uploaded.

### 5. Run the Application

```bash
python app.py
```

The application runs locally on:

```text
http://127.0.0.1:5001
```

---

## 🔄 Working Flow

```text
User
  ↓
Enter Appliance Usage
  ↓
Calculate Energy Consumption
  ↓
Store Energy Data
  ↓
Analyze Morning / Afternoon / Night Usage
  ↓
Identify Peak Usage
  ↓
Calculate Estimated Cost
  ↓
Display Dashboard
  ↓
Check Energy Limit
  ↓
Send Email Alert
  ↓
Show Energy Saving Suggestions
```

---

## 📊 Energy Calculation

The system calculates energy consumption using:

```text
Energy (Units) = Power (Watts) × Time (Hours) / 1000
```

For example:

```text
Power = 100 Watts
Usage = 5 Hours

Energy = (100 × 5) / 1000
       = 0.5 Units
```

---

## 💰 Cost Estimation

The project uses an assumed electricity rate for demonstration:

```text
Electricity Cost = Total Units × Cost Per Unit
```

The current application uses:

```text
₹5 per unit
```

---

## 👩‍💻 Developed By

**Artificial Intelligence & Data Science Team**

* Ch. Ramalakshmi
* K. Nityaprasanthi
* Ch. Gayatri

---

## 🚀 Future Enhancements

* 🤖 Machine Learning-based energy prediction
* 📱 Mobile application
* ☁️ Cloud database integration
* 📈 Monthly and yearly consumption analysis
* 🔔 Real-time notifications
* 🏠 IoT-based smart energy monitoring
* 🌍 Carbon emission estimation
* 📊 Advanced analytics dashboard

---

## 🌍 Impact

The Energy Save System aims to help users understand their electricity consumption and make better energy-use decisions.

> **Save Energy ⚡ Save Money 💰 Save Earth 🌍**

---

<p align="center">
  Made with ❤️ using Python & Flask
</p>

