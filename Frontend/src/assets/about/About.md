# Health Monitor Unit
Health Monitor Unit is an Electrical & Computer Engineering capstone project at Queen's University. The goal of this project is to be able to collect human heartbeat data using an Electrocardiogram (ECG) shield developed for and Arduino microcontroller and display the data on a website for users to view their heartbeat as well as recieve alerts when anomolies are detected through our neural network (NN). The data is then displayed on our Ionic Web App (IWA). Below is the outline of how each component interacts and communicates with each other. 
<img src="assets/about/Structure.png" alt="Structure Diagram" style="margin-top: 10px;" />

## Arduino Electrocardiogram (ECG)
The Arduino ECG is a program that communicates with the [ADS1292R Arduino shield](https://www.protocentral.com/biomedical-shields/818-ads1292r-ecgrespiration-shield-v2.html). It builds off code available from the [ADS1292rShield_Breakout](https://github.com/Protocentral/ADS1292rShield_Breakout) GitHub repository.

## RaspberryPi
The RaspberryPi has many functions:
- Receives serial data from the Arduino ECG
- Sends live heartbeat data to the IWA
- Process heartbeat data into heartbeat segments
- Get presumed classification from NN
- Send alerts to Ionic Web App
- Send training and testing segments to IWA for NN showcase
- Get segments from IWA

Below is how data is transfered within the program:
<img src="assets/about/RaspberryPi.png" alt="RaspberryPi Diagram" style="margin-top: 10px;" />

## Arythmia Neural Network (NN)
The heartbeat analysis neural network is built with PyTorch and used to collect ECG data, parse it into individual heartbeat segments and pass the data through our neural network used to detect issues and anomolies in a user's heartbeat.
<img src="assets/about/Neural Network.png" alt="Neural Network Diagram" style="margin-top: 10px;" />
<img src="assets/about/Results.png" alt="Results Diagram" style="margin-top: 10px;" />

## Web Socket Server
The backend web server uses 'Socket\.Io' and Node.js to open a web-socket server that allows the other components of the solution to communicate with each other. This server predominately functions to redirect data to all connected parties. This server is cloud hosted and publicly accessible through https://backend.healthmonitor.dev.

## Ionic Web App (IWA)
The frontend application is a cross-platform web application developed in Ionic/Angular. It is used to display the heartbeat data provided by the Arduino ECG. This site is cloud hosted and publicly accessible through https://www.healthmonitor.dev.
<img src="assets/about/Ionic Web App.png" alt="Ionic Web App Diagram" style="margin-top: 10px;" />