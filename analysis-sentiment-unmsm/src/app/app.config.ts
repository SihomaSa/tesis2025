// import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
// import { provideRouter } from '@angular/router';
// import { provideHttpClient, withFetch } from '@angular/common/http';
// import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
// import { provideAuth, getAuth, connectAuthEmulator } from '@angular/fire/auth';
// import { provideFirestore, getFirestore } from '@angular/fire/firestore';
// import { provideStorage, getStorage } from '@angular/fire/storage';

// import { routes } from './app.routes';
// import { environment } from '../environments/environment';

// export const appConfig: ApplicationConfig = {
//   providers: [
//     provideZoneChangeDetection({ eventCoalescing: true }),
//     provideRouter(routes),
//     provideHttpClient(),
//     provideFirebaseApp(() => initializeApp(environment.firebase)),
//     provideAuth(() => {
//       const auth = getAuth();
//       // IMPORTANTE: Esto soluciona el error de validación de host
//       if (typeof window !== 'undefined') {
//         (auth as any)._canInitEmulator = false;
//       }
//       return auth;
//     }),
//     provideFirestore(() => getFirestore()),
//     provideStorage(() => getStorage())
//   ]
// };
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch, HTTP_INTERCEPTORS } from '@angular/common/http';
import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
import { provideAuth, getAuth } from '@angular/fire/auth';
import { provideFirestore, getFirestore } from '@angular/fire/firestore';
import { provideStorage, getStorage } from '@angular/fire/storage';
import { routes } from './app.routes';
import { environment } from '../environments/environment';
import { HttpErrorInterceptor } from './core/interceptors/http-error.interceptor';
import { provideAnimations } from '@angular/platform-browser/animations';

// Servicios
import { AuthService } from './core/services/auth.service';  // ✅ Añadido
import { SentimentAnalysisService } from './core/services/sentiment-analysis.service';
import { StatisticsService } from './core/services/statistics.service';
import { ReportsService } from './core/services/reports.service';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(withFetch()),
    provideAnimations(),
    
    // Interceptor HTTP
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpErrorInterceptor,
      multi: true
    },
    
    // Servicios globales
    AuthService,  // ✅ Añadido
    SentimentAnalysisService,
    StatisticsService,
    ReportsService,
    
    // Firebase App
    provideFirebaseApp(() => {
      console.log('🔥 Inicializando Firebase...');
      try {
        const app = initializeApp(environment.firebase);
        console.log('✅ Firebase inicializado correctamente');
        return app;
      } catch (error) {
        console.error('❌ Error inicializando Firebase:', error);
        throw error;
      }
    }),
    
    // Auth
    provideAuth(() => {
      const auth = getAuth();
      console.log('🔑 Servicio de autenticación configurado');
      return auth;
    }),
    
    provideFirestore(() => getFirestore()),
    provideStorage(() => getStorage())
  ]
};