from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='"Hostname or Private IP of AWS Instance":9092')
for _ in range(100):
    producer.send('kafka-social', b'Test Message')
