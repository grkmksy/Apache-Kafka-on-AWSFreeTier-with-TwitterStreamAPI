from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
print("Connecting Remote Kafka Broker on AWS Instance")
consumer = KafkaConsumer('kafka-social',
                         bootstrap_servers=['"Public DNS (IPv4) of AWS Instance":9092'],
                         security_protocol='SSL',
                         ssl_check_hostname=False,
                         ssl_cafile='FilePath/CARoot.pem',
                         ssl_certfile='FilePath/client_certificate.pem',
                         ssl_keyfile=FilePath/client_key.pem',
                         ssl_password='PASSWORD')
print("AWS Kafka Connection Established")
print("Listening")
for msg in consumer:
    data = json.loads(msg.value.decode("UTF-8"))
    print(data)
