# Online-Delivery-Application
A python backend application based on SAGA Architecture with micro-services talking to each other with Kafka Orchestration and MySQL Event Triggers. All services are deployed using Docker and orchestrated using Docker Compose.

# Manual
1) Clone this repository.

2) Run the following commands to get docker images for custom built services -
```
cd buyer
docker build -it buyer .
cd ..
cd restaurant
docker build -it restaurant .
cd ..
cd restaurant_status
docker build -it restaurant_status .
cd ..
```
3) Use Docker-compose to orchestrate the running of all services on the same network
```
cd bitnami
docker-compose up
```
4) Create a Kafka Topic called 'Test' which will be used as the message queue for services to talk to each other
```
docker-compose run kafka /opt/bitnami/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic test
```
5) Start your services once the Kafka Queue is up and running
```
docker-compose run -p 7006:7006 buyer python buyer.py
docker-compose run -p 7007:7007 restaurant_status python restaurant_status.py
docker-compose run restaurant python restaurant.py
```

