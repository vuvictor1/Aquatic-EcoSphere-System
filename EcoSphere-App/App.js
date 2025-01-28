// Authors: Victor Vu and Jordan Morris
// File: app.js
// Description: Mobile app for Aquatic EcoSphere web app.
// Copyright (C) 2025 Victor V. Vu and Jordan Morris
// License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
import React from 'react';
import { SafeAreaView, StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';

const App = () => { // App component
  return ( 
    <SafeAreaView style={styles.container}> 
      <WebView // WebView component to display the web app
        source={{ uri: 'https://aquatic-eco.up.railway.app/' }} // use web app URL
        style={styles.webview}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        startInLoadingState={true}
        allowsInlineMediaPlayback={true}
        mediaPlaybackRequiresUserAction={false}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({ // Set styles
  container: {
    flex: 1,
  },
  webview: {
    flex: 1,
  },
});

export default App; // export App component