<div align="center">
  <img src="https://github.com/user-attachments/assets/99fc8e51-f67f-48bd-ab13-1e6016b9be89" alt="output" width="150"/>
  <h1>Aquatic EcoSphere System</h1>
</div>

**Overview:** (Deployed on [aquatic-eco.up.railway.app ](https://aquatic-eco.up.railway.app/login))

Aquatic EcoSphere is a Python-based system designed to help aquarium owners monitor and manage the health of their aquatic ecosystems. 
Using underwater sensors connected to a Raspberry Pi, the system collects key water parameters such as total dissolved solids, turbidity levels, and temperature. 
This data is sent to a web server, processed in a MySQL database, and displayed through a user interface on both desktop and mobile devices. 
The system provides real-time notifications and educational insights to help users maintain a healthy and sustainable environment for their aquatic life.

## Features:
- **Real-time Monitoring**: Collect and display water parameters for TDS, turbidity levels, and temperature.
- **Push Notifications**: Get alerts when critical water conditions are detected.
- **Educational Insights**: Learn about the biological and chemical factors affecting aquariums.
- **Algorithm Analysis**: Utilize algorithms for interpreting data and providing recommendations.
- **Account Management**: Securely sync tank-specific data across remote locations.
- **Graph Generation**: Visualize collected data for detailed observation.
- **Mobile Support**: Complementary Android application for convenient access to the EcoSphere system.

## Technologies Used:
- Languages: Python, JavaScript, and CSS
- Hardware: Raspberry Pi 5, TDS Sensor, Turbidity Sensor, and Temperature Sensor
- Databases: MySQL, Firestore, and Firebase
- Frameworks: NiceGUI, React Native, Expo, and Tailwind CSS
  
## Run Instructions:
```
python3 main_system.py
```
**For Mobile Type:** 
```
npx expo start
```

## Requirements:
- adafruit_ads1x15==1.0.2
- board==1.0
- fastapi==0.115.6
- nicegui==2.9.1
- PyMySQL==1.1.1
- python-dotenv==1.0.1
- starlette==0.41.3
- w1thermsensor==2.3.0

## Mobile Packages:
- expo: ~52.0.25
- expo-status-bar: ~2.0.1
- react: 18.3.1
- react-native: 0.76.6
- react-native-webview: ^13.13.1
