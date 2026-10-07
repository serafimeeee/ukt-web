-- Jalankan di container db:  mysql < setup_mysql.sql   (ganti password!)
CREATE DATABASE IF NOT EXISTS ukt_db;
CREATE USER IF NOT EXISTS 'userapp'@'%' IDENTIFIED BY 'passwordkamu';
GRANT ALL PRIVILEGES ON ukt_db.* TO 'userapp'@'%';
FLUSH PRIVILEGES;
