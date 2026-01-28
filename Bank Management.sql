use bank;

create table details(
account_number bigint auto_increment primary key,
first_name varchar(55),
last_name varchar(55),
father_or_gardien varchar(55),
phone_number int,   #5
date_of_birth DATE,
age int,
occupation varchar(50),
account_type varchar(50),
aadhar VARCHAR(50),
pan varchar(10),
password_ varchar(255),     #12
deposite_amt int,
withdarwal_amt int,
balance int,
address varchar(300));

alter table details auto_increment = 1555000010027;

select * from details;

drop table details;

ALTER TABLE details
MODIFY phone_number VARCHAR(10);


truncate details;