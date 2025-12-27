// export const environment = {
//   production: true,
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
  production: true,
  firebase: {
    apiKey: "AIzaSyDWjaD5Gvdwg9CogWFPuRb5b1olYDurTVM",
    authDomain: "agripredic.firebaseapp.com",
    projectId: "agripredic",
    storageBucket: "agripredic.firebasestorage.app",
    messagingSenderId: "592931095236",
    appId: "1:592931095236:web:7bed683a4bd9a2d774ff91",
    measurementId: "G-PZWWPXB147"
  },
  // URL de tu API de Machine Learning
  mlApiUrl: 'https://sihomasa-agripredic.hf.space/api/predict',
  
  // Timeouts optimizados
  apiTimeout: 30000, // 30 segundos para ML
  defaultTimeout: 10000 // 10 segundos para otras APIs
};