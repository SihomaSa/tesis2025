import { Component, inject, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { SentimentAnalysisService } from './core/services/sentiment-analysis.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: '<router-outlet></router-outlet>'
})
export class AppComponent implements OnInit {
  
  private router = inject(Router);
  constructor(private sentimentService: SentimentAnalysisService) {}

  ngOnInit() {
    // Verificar autenticación al iniciar
    this.testBackendConnection();

  }

   testBackendConnection() {
    console.log('🧪 Probando conexión con backend...');
    
    this.sentimentService.checkHealth().subscribe({
      next: (response) => {
        console.log('✅ Backend conectado correctamente:', response);
        
        if (response.status === 'healthy') {
          console.log('💚 Sistema saludable');
          console.log('📊 Dataset:', response.dataset_size, 'comentarios');
          console.log('🤖 Modelo:', response.model_accuracy);
        }
      },
      error: (error) => {
        console.error('❌ No se pudo conectar con el backend:', error);
        console.log('💡 Asegúrate de que el backend esté corriendo en http://localhost:8000');
      }
    });
  }
}