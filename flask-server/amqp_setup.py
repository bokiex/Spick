import time
import pika
import os

hostname = os.getenv('HOSTNAME') or "localhost" #localhost
port = os.getenv('HOST_PORT') or 5672         #5672
exchangename = os.getenv('EXCHANGE_NAME') or "create_event_topic" #order_topic
exchangetype = os.getenv('EXCHANGE_TYPE') or "topic" #topic
e_queue_name = os.getenv('ERROR_QUEUE_NAME') or "Error"
n_queue_name = os.getenv('NOTI_QUEUE_NAME') or "Notification"

#to create a connection to the broker
def create_connection(max_retries=12, retry_interval=5):
    print('amqp_setup:create_connection')
    
    retries = 0
    connection = None
    
    # loop to retry connection upto 12 times with a retry interval of 5 seconds
    while retries < max_retries:
        try:
            print('amqp_setup: Trying connection')
            # connect to the broker and set up a communication channel in the connection
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port,heartbeat=3600, blocked_connection_timeout=3600)) 
            print("amqp_setup: Connection established successfully")
            break  # Connection successful, exit the loop
        except pika.exceptions.AMQPConnectionError as e:
            print(f"amqp_setup: Failed to connect: {e}")
            retries += 1
            print(f"amqp_setup: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
            
    if connection is None:
        raise Exception("amqp_setup: Unable to establish a connection to RabbitMQ after multiple attempts.")
    
    return connection

def create_channel(connection):
    print('amqp_setup:create_channel')
    channel = connection.channel()
    # Set up the exchange if the exchange doesn't exist
    print('amqp_setup:create exchange')
    channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True) # 'durable' makes the exchange survive broker restarts
    return channel

#function to create queues
def create_queues(channel):
    print('amqp_setup:create queues')
    create_error_queue(channel)
    create_notification_queue(channel)
    
def create_error_queue(channel):
    print('amqp_setup:create_error_queue')
    channel.queue_declare(queue=e_queue_name, durable=True) # 'durable' makes the queue survive broker restarts
    #bind Error queue
    channel.queue_bind(exchange=exchangename, queue=e_queue_name, routing_key='*.error') 
        # bind the queue to the exchange via the key 'error'

def create_notification_queue(channel):
    print('amqp_setup:create_notification_queue')
    channel.queue_declare(queue=n_queue_name, durable=True) # 'durable' makes the queue survive broker restarts
    #bind Notification queue
    channel.queue_bind(exchange=exchangename, queue=n_queue_name, routing_key='*.notification') 
        # bind the queue to the exchange via the key 'notification'
            
if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')   
    connection = create_connection()
    channel = create_channel(connection)
    create_queues(channel)
    