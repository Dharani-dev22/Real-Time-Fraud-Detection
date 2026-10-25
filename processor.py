import sys
import typing
sys.modules['typing.io'] = typing  # Patch for PySpark on Python 3.13/3.14

import sqlite3
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

os.makedirs("live_transactions", exist_ok=True)
DB_FILE = "fraud_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (tx_id TEXT, timestamp TEXT, user_id TEXT, amount REAL, merchant TEXT, location TEXT, risk_level TEXT)''')
    conn.commit()
    conn.close()

init_db()

spark = SparkSession.builder.appName("FraudDetectionEngine").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

schema = StructType([
    StructField("tx_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("merchant", StringType(), True),
    StructField("location", StringType(), True)
])

df = spark.readStream.schema(schema).json("live_transactions")

fraud_df = df.withColumn("risk_level",
    when(col("amount") > 5000, "High")
    .when((col("amount") > 2000) & (col("merchant").isin("Crypto", "Gaming")), "Medium")
    .otherwise("Low")
)

def write_to_sqlite(batch_df, batch_id):
    pandas_df = batch_df.toPandas()
    if not pandas_df.empty:
        conn = sqlite3.connect(DB_FILE)
        pandas_df.to_sql("transactions", conn, if_exists="append", index=False)
        conn.close()

query = fraud_df.writeStream.foreachBatch(write_to_sqlite).start()
query.awaitTermination()