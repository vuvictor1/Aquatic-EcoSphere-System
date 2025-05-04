<div align="center">
  <img src="https://github.com/user-attachments/assets/99fc8e51-f67f-48bd-ab13-1e6016b9be89" alt="output" width="150"/>
  <h1>Aquatic EcoSphere System</h1>
  <p><strong>Overview:</strong> (Deployed on <a href="https://aquatic-eco.up.railway.app/login">aquatic-eco.up.railway.app</a>)</p>
  <p>Aquatic EcoSphere is a Python-based system designed to help users monitor and manage the health of their aquatic ecosystems. Inspired by the ecological complexity of aquatic environments and the difficulties beginners face in maintaining water stability, the system simplifies maintenance through real-time monitoring, streamlined recommendations, and educational support. Using waterproof sensors connected to a Raspberry Pi 5, the system collects water parameters such as total dissolved solids (TDS), turbidity, and temperature. This data is processed in real-time, stored in a MySQL database, and visualized through a user-friendly interface accessible on both desktop and mobile platforms.</p>
</div>

## Features:
- **Real-time Monitoring**: Collect and display water parameters for TDS, turbidity levels, and temperature.
- **Push Notifications**: Get alerts when critical water conditions are detected.
- **Machine Learning**: A Random Forest model forecasts potential ecosystem instability based on environmental trends.
- **User-Curated Encyclopedia**: Encyclopedia designed to encourage research by journaling data on aquatic species. 
- **Algorithm Analysis**: Utilize customizable algorithms for interpreting data and providing recommendations.
- **Account Management**: Securely sync tank-specific data and settings across remote locations.
- **Graph Generation**: Visualize collected data for detailed observation.
- **Reminders**: Assign critical tasks to be completed by priority. 
- **Mobile Support**: Complementary Android/Apple mobile application for convenient access to the EcoSphere system.

## Technologies Used:
- Languages: Python, JavaScript, and CSS
- Hardware: Raspberry Pi 5, TDS Sensor, Turbidity Sensor, and Temperature Sensor
- Databases: MySQL and Expo Push Notifications
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
- fastapi==0.115.12
- nicegui==2.9.1
- numpy==2.2.5
- pandas==2.2.3
- PyMySQL==1.1.1
- python-dotenv==1.1.0
- Requests==2.32.3
- scikit_learn==1.6.1
- starlette==0.41.3
- w1thermsensor==2.3.0

## Mobile Packages:
- "expo": "~52.0.35",
- "expo-constants": "^17.0.8",
- "expo-notifications": "^0.29.14",
- "react": "18.3.1",
- "react-native": "0.76.9",
- "react-native-webview": "13.12.5"
