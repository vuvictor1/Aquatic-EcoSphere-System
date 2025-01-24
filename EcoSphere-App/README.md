# EcoSphere App - Expo Go Setup Guide

This guide will walk you through the steps to run the EcoSphere app on your mobile device using Expo Go. Follow the instructions below to get started.

## Prerequisites

Before you begin, ensure you have the following:

- A smartphone (Android or iOS).
- The Expo Go app installed on your phone:
  - [Download Expo Go for Android](https://expo.dev/client)
  - [Download Expo Go for iOS](https://expo.dev/client)

## Step 1: Install Dependencies

1. Open a terminal or command prompt.
2. Navigate to the EcoSphereApp directory:
    ```bash
    cd EcoSphereApp
    ```
3. Install the required dependencies by running:
    ```bash
    npm install
    ```

## Step 2: Start the Expo Development Server

1. In the EcoSphereApp directory, start the Expo development server:
    ```bash
    npm start
    ```
2. This will open the Expo Dev Tools in your browser.

## Step 3: Run the App on Your Phone

1. Open the Expo Go app on your phone.
2. Scan the QR code displayed in the Expo Dev Tools:
    - **On Android:** Use the Scan QR Code option in the Expo Go app.
    - **On iOS:** Use the Camera app to scan the QR code, then tap the notification to open the app in Expo Go.

## Step 4: Test the App

Once the app loads in Expo Go, you should see the EcoSphere app running. Test the following:

- Navigate through the app (e.g., Home, Graphs, Settings, etc.).
- Ensure all functionalities (e.g., forms, buttons, graphs) work as expected.

## Troubleshooting

### App Not Loading

- Ensure your phone and computer are connected to the same Wi-Fi network.
- Restart the Expo development server:
    ```bash
    npm start
    ```

### QR Code Not Scanning

- Make sure your phone’s camera is working properly.
- Manually enter the connection URL displayed in the Expo Dev Tools into the Expo Go app.

### Clear Cache

If the app behaves unexpectedly, clear the Expo cache:
    ```bash
    expo start -c
    ```

## Additional Notes

- If you want to run the app on an emulator or simulator, let me know, and I can guide you through that process.
- For any questions or issues, feel free to reach out to me.

Enjoy exploring the EcoSphere app! 🌊

---

Here is an installable compiled APK for Android: [Download APK](https://drive.google.com/file/d/1dmjD0jPCN5wNeuN0vdfwAFw5_GDsrUUL/view?usp=sharing)

To build your own APKs, run:
```bash
npx eas build --platform android