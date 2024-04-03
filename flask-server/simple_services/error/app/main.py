import amqp_connection
import json
import pika
from os import environ
from os import environ
from dotenv import load_dotenv 
from datetime import datetime

load_dotenv()
e_queue_name = environ.get('ERROR_QUEUE_NAME') or "Error" #Error


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
    with open("errorlogs.txt","a+") as f:
        now = datetime.now()
        cur_time = now.strftime("%H:%M:%S")
        f.write(cur_time + "Error microservice: Received an error by " + __file__ + "    " + processError(body) + "\ns")
    print()
    
def processError(errorMsg):
    print("Error microservice: Printing the error message:")
    try:
        error = json.loads(errorMsg)
        print("--JSON:", error)
        return "--JSON " + error
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", errorMsg)
        print()
        return "--NOT JSON:" + e + "--DATA:" + errorMsg
    
if __name__ == "__main__":
    print("Error microservice: Getting Connection")
    connection = amqp_connection.create_connection()
    print("Error microservice: Connection established successfully")
    channel = connection.channel()
    receiveError(channel)