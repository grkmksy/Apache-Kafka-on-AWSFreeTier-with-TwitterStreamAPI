# Apache-Kafka-on-AWS
Apache Kafka Operations on AWS Free Tier Instance

Kafka Broker Integration with Local Host
===================

Apache Kafka is an open source, distributed messaging system that enables you to build real-time applications using streaming data. With this integration you can stream data to your local host from AWS instances via SSL. 


# Launch a Linux Virtual Machine on AWS EC2 Free Tier

  Please follow the instructions on the link below. (**Plesase Select Ubuntu Server 16.04 LTS as Free Tier Operating System**)
  > **https://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine**
  
  Once you have successfully created the virtual machine, proceed with the operations listed below. 
  - Connect to instance.
  - Install Java OpenJDK
```sh
$ sudo apt-get update
$ sudo apt-get install openjdk-8-jdk
```
 - Install pip3 (Python 3.5.2 installed as default) & Install kafka-python
```sh
$ sudo apt install python3-pip
$ sudo pip3 install kafka-python
```
 # Download & Install Apache Kafka
> Download Apache Kafka https://kafka.apache.org/downloads

Once you have successfully downloaded Apache Kafka binary, proceed with the operations listed below. 
 - Extract & Rename Apache Kafka Folder
```sh
$ tar -xzf kafka_2.11-1.0.0.tgz
$ mv kafka_2.11-1.0.0.tgz kafka
$ cd kafka
```

# Configure AWS EC2 Free Tier Security Group for Apache Kafka Port Listening
- Find and click **Securiy Groups** section under **Network & Security** in AWS EC2 Dashboard.
- Select security group which is your instance included.
- Edit this group's inbound and outbound rules as below. 

|  |  |
| ------ | ------ |
| Type | Custom TCP Rule |
| Protocol | TCP |
| Port Range | 2181 |
| Source | My IP (which is your IP) |
| Description | ZooKeeper Connection |

|  |  |
| ------ | ------ |
| Type | Custom TCP Rule |
| Protocol |TCP |
| Port Range | 9092 |
| Source | My IP (which is your IP) |
| Description | Kafka Connection |

> Detailed information about Security Groups http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_SecurityGroups.html#VPCSecurityGroups

# Configure AWS EC2 Free Tier Network 
If you associate your instance with an Elastic IP, your crawler will be work more properly, against connection problems.
>An Elastic IP address is a static IPv4 address designed for dynamic cloud computing. An Elastic IP address is associated with your AWS account. With an Elastic IP address, you can mask the failure of an instance or software by rapidly remapping the address to another instance in your account. An Elastic IP address is a public IPv4 address, which is reachable from the Internet. If your instance does not have a public IPv4 address, you can associate an Elastic IP address with your instance to enable communication with the Internet; for example, to connect to your instance from your local computer.

- Find and click **Elastic IPs** section under **Network & Security** in AWS EC2 Dashboard.
- Allocate new address
- Select newly allocated Elastic IP and associate it with your instance
 **Note: If you allocated an Elastic IP, you must be associate with an instance. Otherwise, there will be some financial charge for allocating Elastic IP uncessearily. If you do not use IP, please release it.**

# Kafka + SSL Integration - Generate SSL Key and Certificate of Kafka Broker
**Server Certificate Setup**
Create folder named ssl in kafka folder.
```sh
$ cd kafka/
$ mkdir ssl
$ cd ssl/
```
Create Certificate Authority
```sh
$ openssl req -new -x509 -keyout ca-key -out ca-cert -days 365
```
Create Server Keystore 
```sh
$ keytool -keystore server.keystore.jks -alias server -validity 3650 -genkey -keyalg RSA
```
Trust CA - Server Side 
```sh
$ keytool -keystore server.truststore.jks -alias CARoot -import -file ca-cert
```
Extract Server Certificate From Keystore 
```sh
$ keytool -keystore server.keystore.jks -alias server -certreq -file cert-file-server
```
Sign Server Certificate with CA 
```sh
$ openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file-server -out cert-signed-server -days 3650 -CAcreateserial -passin pass:"Enter Password"
```
Import CA Certficate to Keystore 
```sh
$ keytool -keystore server.keystore.jks -alias CARoot -import -file ca-cert
```
Import Signed Server Certificate to Server
```sh
$ keytool -keystore server.keystore.jks -alias server -import -file cert-signed-server
```
**Client Certificate Setup**
Create Client Keystore 
```sh
$ keytool -keystore client.keystore.jks -alias client -validity 3650 -genkey -keyalg RSA
```
Trust CA - Client Side 
```sh
$ keytool -keystore client.truststore.jks -alias CARoot -import -file ca-cert
```
Extract Client Certificate From Keystore 
```sh
$ keytool -keystore client.keystore.jks -alias client -certreq -file cert-file-client
```
Sign Client Certificate with CA 
```sh
$ openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file-client -out cert-signed-client -days -CAcreateserial -passin pass:"Enter Password"
```
Import CA Certficate to Keystore 
```sh
$ keytool -keystore client.keystore.jks -alias CARoot -import -file ca-cert
```
Import Signed Client Certificate to Server
```sh
$ keytool -keystore client.keystore.jks -alias client -import -file cert-signed-client
```

**Extract Required Keys and Certificates**

Extract Client Cerfiticate
```sh
$ keytool -exportcert -alias client -keystore client.keystore.jks -rfc -file client_certificate.pem
```
Convert Keystore to PKCS12 file in order to
extract the private key
```sh
$ keytool -v -importkeystore -srckeystore client.keystore.jks -srcalias client -destkeystore
cert_and_key.p12 -deststoretype PKCS12
```
This command only prints the key. You have to copy the **inclusive** between --BEGIN PRIVATE KEY-- and --END PRIVATE KEY -- to new file called client_key.pem
```sh
$ openssl pkcs12 -in cert_and_key.p12 -nocerts -nodes
$ Copy the **inclusive** between --BEGIN PRIVATE KEY-- and --END PRIVATE KEY --
$ nano client_key.pem
$ CTRL+LEFT SHIFT+V
$ CTRL+X+Y - Enter
```
Extract The CARoot Certificate
```sh
$keytool -exportcert -alias CARoot -keystore client.keystore.jks -rfc -file CARoot.pem
```

 # Apache Kafka Producer & Consumer Examples in Python Language
 **Dependencies**
 - Python3.0=<
 - kafka-python Library
 
**Kafka Simple Producer Example**
```sh
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='"Hostname or Private IP of AWS Instance":9092')
for _ in range(100):
    producer.send('kafka-social', b'Test Message')
```

**Kafka Simple Consumer Example**
```sh
from kafka import KafkaConsumer
consumer = KafkaConsumer('kafka-social',
                         group_id='my-group',
                         bootstrap_servers=['"Public DNS (IPv4) of AWS Instance":9092'])

print("Listening")
for msg in consumer:
    print(msg)
```

**Kafka Producer Example with SSL**
```sh
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
```
**Kafka Consumer Example with SSL**
```sh
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
```

# Apache Kafka Server Properties Configurations
 - Go to Apache Kafka Directory
```sh
$ cd kafka
```
- Edit config/server.properties with your favorite text editor
```sh
$ nano config/server.properties
```
- Add below commands to end of file
```sh
# The address the socket server listens on.
$ listeners=SSL://"Hostname or Private IP of AWS Instance":9092
# Enable SSL for inter-broker communication
$ inter.broker.listener.name=SSL
# Hostname and port the broker will advertise to producers and consumers.
$ advertised.listeners=SSL://"Hostname or Private IP of AWS Instance":9092
# SSL Files Locations and Passwords
$ ssl.keystore.location=FilePath/server.keystore.jks
$ ssl.keystore.password=PASSWORD.
$ ssl.key.password=PASSWORD.
$ ssl.truststore.location=FilePath/server.truststore.jks
$ ssl.truststore.password=PASSWORD
```
- Save and Exit File
```sh
$ CTRL + X + Y - Enter
```

# Run Apache Kafka Broker
 - Start Apache Kafka Broker on AWS Free Tier with Java 512MB Java Heap Size
```sh
$ cd kafka
$ bin/zookeeper-server-start.sh config/zookeeper.properties
$ export KAFKA_HEAP_OPTS="-Xmx512m -Xms512m"
$ bin/kafka-server-start.sh config/server.properties
```
- List Active Topics
```sh
$ bin/kafka-topics.sh --list --zookeeper localhost:2181
```

**Now you can send data your Kafka Topic on your AWS Free Tier**
