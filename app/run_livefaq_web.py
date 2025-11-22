# run_livefaq_full.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from transformers import pipeline
from pymongo import MongoClient
import json

# Initialize Spark
spark = SparkSession.builder \
    .appName("LiveFAQ Pipeline") \
    .master("local[*]") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/livefaq.responses") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Load NLP Model (Q/A)
qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

client = MongoClient("mongodb://localhost:27017/")
db = client["livefaq"]
collection = db["responses"]

def answer_question(text):
    try:
        context = "This is a live FAQ answering system built using Big Data tools."
        result = qa_model(question=text, context=context)
        return result["answer"]
    except:
        return "Unable to answer."

answer_udf = udf(answer_question)

# Read from Kafka
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "livefaq_raw") \
    .load()

# Parse JSON
json_df = raw_df.selectExpr("CAST(value AS STRING) AS json")
clean_df = json_df.selectExpr("json_tuple(json, 'username', 'message', 'timestamp') as row")

split_df = clean_df.selectExpr(
    "get_json_object(row, '$.username') AS username",
    "get_json_object(row, '$.message') AS message",
    "get_json_object(row, '$.timestamp') AS timestamp"
)

# Add model response
result_df = split_df.withColumn("answer", answer_udf(col("message")))

def save_to_mongo(row):
    rec = {
        "username": row.username,
        "question": row.message,
        "answer": row.answer,
        "timestamp": row.timestamp
    }
    collection.insert_one(rec)

query = result_df.writeStream \
    .foreach(save_to_mongo) \
    .outputMode("update") \
    .start()

query.awaitTermination()
