# Real-Time Financial Fraud Detection Engine 🚨

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-PySpark-orange.svg)](https://spark.apache.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Dashboard-FF4B4B.svg)](https://streamlit.io/)

**Live Project Dashboard:** [dharani-soc-dashboard.streamlit.app](https://dharani-soc-dashboard.streamlit.app/)

A real-time Big Data streaming pipeline designed to ingest, process, and visualize high-velocity financial transactions to detect fraudulent activity instantly without relying on costly cloud infrastructure. Developed as a Third Year IT (TYIT) Academic Project.

---

## 🏗️ System Architecture

The architecture consists of three decoupled components running concurrently:

1. **Data Firehose (`generator.py`):** A Python daemon simulating a live stream of credit card transactions across global cities, writing JSON events to a local directory at high velocity.
2. **Big Data Engine (`processor.py`):** An Apache Spark (PySpark) Structured Streaming application that continuously monitors the ingestion directory, evaluates rule-based risk thresholds, and appends the processed ledger to a local SQLite database.
3. **SOC Dashboard (`app.py`):** A Streamlit web application providing a live, auto-refreshing interface for security analysts to monitor transaction velocity, geographic hotspots, and intercepted threats.

---

## 🚀 Features

* **High-Throughput Ingestion:** Simulates live global financial transaction networks.
* **Distributed Stream Processing:** Utilizes PySpark `readStream` and `writeStream` to handle unbounded data with zero latency.
* **Rule-Based Risk Evaluation:** Automatically flags transactions over $5000 as "High Risk" and specific high-volume merchant categories (e.g., Crypto, Gaming) as "Medium Risk".
* **Live SOC Dashboard:** Real-time data visualization featuring geographic threat mapping, pie charts, and events-per-second velocity tracking using Plotly.
* **CSV Export Forensics:** Download filtered threat logs directly from the dashboard for offline analysis.

---

## 🛠️ Technologies Used

* **Language:** Python
* **Data Processing:** Apache Spark (PySpark)
* **Database:** SQLite
* **Frontend UI:** Streamlit
* **Visualizations:** Plotly Express

---

## ⚙️ Installation & Setup

### Prerequisites
* **Python 3.10+** installed on your system.
* **Java Development Kit (JDK 8 or 11)** installed and added to your system's PATH (Required for the PySpark JVM).

### 1. Clone the Repository
```bash
git clone https://github.com/Dharani-dev22/Real-Time-Fraud-Detection.git
cd Real-Time-Fraud-Detection
```

### 2. Install Dependencies
It is recommended to use a virtual environment.
```bash
pip install pyspark pandas streamlit plotly
```

---

## 💻 Usage Instructions

Because the system relies on decoupled streaming architecture, you must run all three scripts simultaneously in **three separate terminal windows**.

**Terminal 1: Start the Data Firehose**
Generates live JSON transactions.
```bash
python generator.py
```

**Terminal 2: Start the PySpark Processor**
Ingests the JSON files and writes processed data to SQLite.
```bash
python processor.py
```

**Terminal 3: Launch the SOC Dashboard**
Starts the Streamlit frontend.
```bash
streamlit run app.py
```

---

## 📸 Dashboard Screenshots

*(Ensure `dashboard_top.png` and `dashboard_bottom.png` are uploaded to your repository to display these images)*

### Live SOC Controls & Geographic Hotspots
![SOC Dashboard Top](dashboard_top.png)

### Transaction Velocity & Processed Ledger
![SOC Dashboard Bottom](dashboard_bottom.png)

---

## 👨‍💻 Author

**Pondharani Devendra**  
*B.Sc. Information Technology (TYIT)*  
SIWS College, University of Mumbai  
*Project Guide: Ms. Gayatri Venkatachalam*
