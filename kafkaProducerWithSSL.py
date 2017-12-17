from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
producer = KafkaProducer(bootstrap_servers=['"Hostname or Private IP of AWS Instance":9092'],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                         security_protocol='SSL',
                         ssl_check_hostname=False,
                         ssl_cafile='/home/ubuntu/kafka/ssl/CARoot.pem',
                         ssl_certfile='/home/ubuntu/kafka/ssl/client_certificate.pem',
                         ssl_keyfile='/home/ubuntu/kafka/ssl/client_key.pem',
                         ssl_password='PASSWORD')
print("Cluster Kafka Connection Established")
