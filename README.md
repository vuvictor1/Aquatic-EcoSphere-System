# Aquatic EcoSphere System
Monitoring tool for managing optimal conditions in aquatic ecosystems through real-time sensor data, educational insights, and algorithm-driven analysis.

Deployment: [aquatic-eco.up.railway.app ](https://aquatic-eco.up.railway.app/login)

**Overview:**

Aquatic EcoSphere is a Python-based system designed to help aquarium owners monitor and manage the health of their aquatic ecosystems. Using underwater sensors connected to a Raspberry Pi, the system collects key water parameters such as temperature, total dissolved solids, and turbidity levels. This data is sent to a local web server, processed in a MySQL database, and displayed through a user interface on both desktop and mobile devices. The system provides real-time notifications and educational insights to help users maintain a healthy and sustainable environment for their aquatic life.

**Features:**
- **Real-time Monitoring**: Collect and display water parameters temperature, TDS, and turbidity levels.
- **Push Notifications**: Get alerts when critical water conditions are detected.
- **Educational Insights**: Learn about the biological and chemical factors affecting aquariums.
- **Algorithm Analysis**: Utilize algorithms for interpreting data and providing recommendations.
- **Account Management**: Securely sync tank-specific data across remote locations.
- **Graph Generation**: Visualize collected data for user insights.
- **Mobile Support**: Complementary Android application for convenient access to the EcoSphere system.

**Technologies Used:**
- Python
- JavaScript
- Raspberry Pi 5
- MySQL
- Firestore
- Firebase
- NiceGUI
- React Native
- Expo
  
***Run Instructions:*** Type
```
python3 main_system.py
```

***Requirements:***
- adafruit_ads1x15==1.0.2
- board==1.0
- fastapi==0.115.6
- nicegui==2.9.1
- PyMySQL==1.1.1
- python-dotenv==1.0.1
- starlette==0.41.3
- w1thermsensor==2.3.0

- "expo": "~52.0.25",
- "expo-status-bar": "~2.0.1",
- "react": "18.3.1",
- "react-native": "0.76.6",
- "react-native-webview": "^13.13.1"
