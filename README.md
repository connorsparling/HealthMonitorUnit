# Health Monitor Unit
Health Monitor Unit is an Electrical & Computer Engineering capstone project at Queen's University. The goal of this project is to be able to collect human heartbeat data using an Electrocardiogram (ECG) shield developed for and Arduino microcontroller and display the data on a website for users to view their heartbeat as well as recieve alerts when anomolies are detected through our neural network. Below is the outline of how each component interacts together. 
<img src="Resources/Communication Diagram.png" alt="Communication Diagram" style="margin-top: 10px;" />

## Arduino Electrocardiogram (ECG) <span style="font-size: 16px;">[(Read More)](ArduinoECG/README.md)</span>
The Arduino ECG is a program that communicates with the [ADS1292R Arduino shield](https://www.protocentral.com/biomedical-shields/818-ads1292r-ecgrespiration-shield-v2.html). It builds off code available from the [ADS1292rShield_Breakout](https://github.com/Protocentral/ADS1292rShield_Breakout) GitHub repository.

## Web Socket Server <span style="font-size: 16px;">[(Read More)](Backend/README.md)</span>
The backend web server uses 'Socket\.Io' and Node.js to open a web-socket server that allows the other components of the solution to communicate with each other. This server is cloud hosted and publicly accessible through https://backend.healthmonitor.dev.

## Arythmia Neural Network <span style="font-size: 16px;">[(Read More)](neuralNetwork/README.md)</span>
The heartbeat analysis neural network is built with PyTorch and used to collect ECG data, parse it into individual heartbeat segments and pass the data through our neural network used to detect issues and anomolies in a user's heartbeat.

## Ionic Web App <span style="font-size: 16px;">[(Read More)](Frontend/README.md)</span>
The frontend application is a cross-platform web application developed in Ionic/Angular. It is used to display the heartbeat data provided by the Arduino ECG. This site is cloud hosted and publicly accessible through https://www.healthmonitor.dev.
