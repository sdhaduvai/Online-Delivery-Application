CREATE DATABASE test_db;
use test_db;
create table customer(userId int primary key, name varchar(40));
create table restaurant(restId INTEGER primary key, name varchar(40));
create table orders(uuid varchar(40) PRIMARY KEY, cust_id INTEGER, rest_id INTEGER, status varchar(20), dish varchar(20), FOREIGN KEY (cust_id) references customer(userId), FOREIGN KEY (rest_id) references restaurant(restId));