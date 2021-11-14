# Webapp_server_with_Flask
 Web app server which communicate with firebase, using Python, Flask, Apache.
 <br />
 The goal of this project is implementing webapp server which communicates with Arduino, Firebase Realtime Database.
 Arduino is connected with WiFi module(ESP-8086-01) and gives some information to Pi webapp server.
 Firebase push notification alarm when realtime database is renewed.
 
 * run.py : Communication with client(Arduino), access to MySQL, and Update the fire information.
 * mySQL.py : Establishes a connection to MySQL and executes a query for HTTP requests.
 * fire.py : When emergencyu situation is occured, the situation is saved in server and send emergency push alarm to Google Firebase.
 * bs.py : Beautiful Soup, a Python library that parses HTML, crawls Naver weather information and update it.
 * templates : HTTP templates.
 * info : files containing a information such as emergency situation, weather information.
 
 <br />
 <br />

# What this code does is
 * HTTP communication with Arduino (GET type)
 * Realtime Database data upload
 * HTTP Communication using Python Flask
 * Notifying multiple devices using Data request
 * DB Access using pymysql

 <br />
 <br />

# Brief Setup guide for RaspberryPi
## Install Raspbian
 This project works using Raspiban OS.
 You can download an install file on site below :
 ```
 https://www.raspberrypi.org/downloads/raspbian/
 ```
 <br />
 <br />

## Conneting with SSH, mstsc (Window OS)
 First of all, we should make remote development environments, using PuTTY or mstsc(Window).
 If you don't need, you can skip this chapter.
 <br />

### 1) Router Port Forwarding
 You should set port forwarding option when you use router.
 Router assigns inner "virtual" ip address to your RaspberryPi so extern computer or clients cannot find you.
 Clients must access through your router ip address and certain port number,
 then router interprets the request (make connection with your Pi), finally, clients can communicate with Pi.
 This is port forwarding.

### 2) Raspbian Firewall Configuration
 I think that your Pi initially installed the firewall when you downloaded raspbian OS full package.
 If not, you can install the firewall using this code. Just type it!
 ```
 sudo apt-get install ufw
 ```
 <br />

 After installing the firewall, you should check the version is latest one. Use this codes.
 ```
 sudo apt-get upgrade
 sudo apt-get update
 ```
 <br />

 You can check firewall status using this command, shown below :
 ```
 sudo ufw status
 ```
 <br />

 If you want to allow certain port on your Pi, type this.
 ```
 sudo ufw allow 22
 // this command allows tcp/udp communication on #22 port.

 sudo ufw allow 22/tcp
 // this command allows only tcp communication on #22 port.
 ```
 <br />

 If you want to deny some ports, type this.
 ```
 sudo ufw deny 22/tcp
 // this command deny only tcp communication on #22 port.
 ```
 <br />

 You can delete rule.
 ```
 sudo ufw delete allow 22/tcp
 // this command will delete 'allow 22/tcp' rule.
 ```
 <br />

 SSH use #22 port as default, mstsc(vnc) use #3389 port as default.
 You should open this ports.
 <br />

### 3) Allow SSH, VNC on raspi-config
 Type this command on your terminal.
 ```
 sudo raspi-config
 ```
 <br />

 You should allow SSH, VNC on raspi-config.
