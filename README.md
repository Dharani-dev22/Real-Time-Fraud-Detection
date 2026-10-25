# Distributed Threat Intelligence & Log Analyzer

## Architecture
Kafka -> PySpark -> MongoDB -> Streamlit

## Prerequisites
Docker, Docker Compose, Python 3.8+

## Setup Instructions
1. Start Infrastructure:
   docker-compose up -d
2. Install Dependencies:
   pip install -r requirements.txt
3. Run Data Generator (Terminal 1):
   python generator.py
4. Run Spark Processor (Terminal 2):
   python processor.py
5. Run Streamlit Dashboard (Terminal 3):
   streamlit run app.py
