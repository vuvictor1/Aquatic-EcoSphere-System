EcoSphere App - Expo Go Setup Guide
This guide will walk you through the steps to run the EcoSphere app on your mobile device using Expo Go. Follow the instructions below to get started.

Prerequisites
Before you begin, ensure you have the following:

A smartphone (Android or iOS).
The Expo Go app installed on your phone:
Download Expo Go for Android
Download Expo Go for iOS
Step 1: Install Dependencies
Open a terminal or command prompt.
Navigate to the EcoSphereApp directory:
bash
Insert Code
Run
Copy code
cd EcoSphereApp
Install the required dependencies by running:
bash
Insert Code
Run
Copy code
npm install
Step 2: Start the Expo Development Server
In the EcoSphereApp directory, start the Expo development server:
bash
Insert Code
Run
Copy code
npm start
This will open the Expo Dev Tools in your browser. It should look something like this:Expo Dev Tools
Step 3: Run the App on Your Phone
Open the Expo Go app on your phone.
Scan the QR code displayed in the Expo Dev Tools:
On Android: Use the Scan QR Code option in the Expo Go app.
On iOS: Use the Camera app to scan the QR code, then tap the notification to open the app in Expo Go.
Step 4: Test the App
Once the app loads in Expo Go, you should see the EcoSphere app running. Test the following:

Navigate through the app (e.g., Home, Graphs, Settings, etc.).
Ensure all functionalities (e.g., forms, buttons, graphs) work as expected.
Troubleshooting
If you encounter any issues:

App Not Loading:
Ensure your phone and computer are connected to the same Wi-Fi network.
Restart the Expo development server (npm start).
QR Code Not Scanning:
Make sure your phone’s camera is working properly.
Manually enter the connection URL displayed in the Expo Dev Tools into the Expo Go app.
Clear Cache: If the app behaves unexpectedly, clear the Expo cache:
bash
Insert Code
Run
Copy code
expo start -c
Additional Notes
If you want to run the app on an emulator or simulator, let me know, and I can guide you through that process.
For any questions or issues, feel free to reach out to me.
Enjoy exploring the EcoSphere app! 🌊

------------------
Thanks for taking the time to write out these instructions!

Here is a installable compiled apk for android: https://drive.google.com/file/d/1dmjD0jPCN5wNeuN0vdfwAFw5_GDsrUUL/view?usp=sharing

To build your own APKs type: npx eas build --platform android