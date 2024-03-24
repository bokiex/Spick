import amqp_connection
import json
import pika
from os import environ
from fastapi import FastAPI, Depends
from datetime import datetime
from invokes import invoke_http
from os import environ
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

e_queue_name = environ.get('Error') or "Error" #Error

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Error microservice: Getting Connection")
    connection = amqp_connection.create_connection()
    print("Error microservice: Connection established successfully")
    channel = connection.channel()
    receiveError(channel)
    yield
    connection.close()

def receiveError(channel):
    try:
        channel.basic_consume(queue=e_queue_name, on_message_callback=callback, auto_ack=True)
        print('Error microservice: Consuming from queue:', e_queue_name)
        channel.start_consuming()
        
    except pika.exceptions.AMQPError as e:
        print(f"Error microservice: Failed to connect: {e}")
        
    except KeyboardInterrupt:
        print("Error microservice: Program interrupted by user.")
        
        
def callback(channel, method, properties, body):
    print("\nError microservice: Received an error by " + __file__)
    processError(body)
    print()
    
def processError(errorMsg):
    print("Error microservice: Printing the error message:")
    try:
        error = json.loads(errorMsg)
        print("--JSON:", error)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", errorMsg)
    print()
    
if __name__ == "__main__":
    print("Error microservice: Getting Connection")
    connection = amqp_connection.create_connection()
    print("Error microservice: Connection established successfully")
    channel = connection.channel()
    receiveError(channel)