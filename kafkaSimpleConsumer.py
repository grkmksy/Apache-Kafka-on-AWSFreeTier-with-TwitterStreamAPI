from kafka import KafkaConsumer
consumer = KafkaConsumer('kafka-social',
                         group_id='my-group',
                         bootstrap_servers=['"Public DNS (IPv4) of AWS Instance":9092'])

print("Listening")
for msg in consumer:
    print(msg)
