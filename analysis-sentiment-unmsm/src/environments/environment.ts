// export const environment = {
//   production: false,
//   firebase: {
//     apiKey: "AIzaSyDWjaD5Gvdwg9CogWFPuRb5b1olYDurTVM",
//     authDomain: "agripredic.firebaseapp.com",
//     projectId: "agripredic",
//     storageBucket: "agripredic.firebasestorage.app",
//     messagingSenderId: "592931095236",
//     appId: "1:592931095236:web:7bed683a4bd9a2d774ff91",
//     measurementId: "G-PZWWPXB147"
//   }
// };
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
  
  // NUEVO: URL de tu backend local FastAPI
  backendUrl: 'http://localhost:8000/api',
  
  // URL de tu API de Machine Learning alternativa (Hugging Face)
  mlApiUrl: 'https://sihomasa-analysis-sentiment-unmsm.hf.space/api/predict',
  
  // Usar backend local por defecto
  useLocalBackend: true, // Cambiar a false para usar Hugging Face
  
  // Timeouts optimizados
  apiTimeout: 30000, // 30 segundos para ML
  defaultTimeout: 10000 // 10 segundos para otras APIs
};