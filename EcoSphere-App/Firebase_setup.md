 Setup Instructions for Firebase Cloud Messaging
Follow these steps to replicate the setup for Firebase Cloud Messaging in this project.

1️⃣ Clone the Repository
Clone this repository from GitHub:

bash
Copy
Edit
git clone <repository-url>
cd <project-directory>
Install all necessary dependencies:

Frontend (React):
bash
Copy
Edit
cd frontend/
npm install
Backend (Python):
bash
Copy
Edit
cd backend/
pip install -r requirements.txt
2️⃣ Add the Firebase Configuration Files
Some critical files were excluded from the repository for security reasons (e.g., .env, firebase_service_account.json). You will need to set these up manually.

⚙️ Frontend Configuration
Go to the Firebase Console:

Navigate to your project.
Under Project Settings → General → Your Apps, copy the Firebase config object.
Create a firebase.js file in the src/ folder of the React app:

javascript
Copy
Edit
import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

export const requestForToken = async () => {
  try {
    const token = await getToken(messaging, {
      vapidKey: "YOUR_PUBLIC_VAPID_KEY",
    });
    if (token) {
      console.log("FCM Token:", token);
      return token;
    } else {
      console.log("No registration token available.");
    }
  } catch (error) {
    console.error("An error occurred while retrieving token:", error);
  }
};

export const onMessageListener = () =>
  new Promise((resolve) => {
    onMessage(messaging, (payload) => {
      resolve(payload);
    });
  });
Replace YOUR_PUBLIC_VAPID_KEY with the Public VAPID Key from Firebase Console under Cloud Messaging.

Push the updated React app to the hosting service (e.g., Railway).

⚙️ Backend Configuration
Download the Service Account JSON file:

Go to Firebase Console → Project Settings → Service Accounts → Generate New Private Key.
Save the file as firebase_service_account.json.
Create a .env file in the backend/ directory and add:

makefile
Copy
Edit
FIREBASE_VAPID_PRIVATE_KEY=your_vapid_private_key_here
Ensure the firebase_service_account.json is in the config/ folder.

3️⃣ Set Up Environment Variables
Since some sensitive information (e.g., keys) is excluded, you'll need to manually set up environment variables.

Frontend:
No .env file is needed since the Firebase configuration is already embedded in firebase.js.
Backend:
Install python-dotenv to handle environment variables:

bash
Copy
Edit
pip install python-dotenv
Ensure the .env file contains:

makefile
Copy
Edit
FIREBASE_VAPID_PRIVATE_KEY=your_private_key
4️⃣ Run the Project
Start the Backend:
Navigate to the backend folder:
bash
Copy
Edit
cd backend/
Run the backend server:
bash
Copy
Edit
python app.py
Start the Frontend:
Navigate to the frontend folder:
bash
Copy
Edit
cd frontend/
Run the React app:
bash
Copy
Edit
npm start
🧪 Testing Notifications
On the React Frontend:
Allow notification permissions in your browser.
Open the browser console to check if the FCM token is logged.
On the Python Backend:
Use the token received from the React app to send a test notification:

python
Copy
Edit
def send_push_notification(token, title, body):
    from firebase_admin import messaging
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    response = messaging.send(message)
    print("Successfully sent message:", response)

# Replace with a valid FCM token
send_push_notification("your_fcm_token", "Test Notification", "Hello, World!")
Confirm that the notification appears in the browser.

📄 File Summary
File Name	Purpose
firebase_service_account.json	Service Account credentials for Firebase Admin SDK.
.env	Contains sensitive data like the VAPID private key.
firebase.js	Initializes Firebase in the React frontend.