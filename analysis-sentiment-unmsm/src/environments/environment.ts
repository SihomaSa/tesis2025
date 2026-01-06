export const environment = {
  production: false,
  
  firebase: {
    apiKey: "AIzaSyDWjaD5Gvdwg9CogWFPuRb5b1olYDurTVM",
    authDomain: "analysis-sentiment-unmsm.firebaseapp.com",
    projectId: "analysis-sentiment-unmsm",
    storageBucket: "analysis-sentiment-unmsm.firebasestorage.app",
    messagingSenderId: "1095818411160",
    appId: "1:1095818411160:web:fb530e36e049fc66f424ed",
    measurementId: "G-MCJV4MTVW8"
  },
  
  // URLs del backend - CORREGIDAS
  backendUrl: 'http://localhost:8000/api',
  apiUrl: 'http://localhost:8000/api',  // Consistente con backendUrl
  mlApiUrl: 'http://localhost:8000',
  
  useLocalBackend: true,
  apiTimeout: 30000,
  defaultTimeout: 10000
};