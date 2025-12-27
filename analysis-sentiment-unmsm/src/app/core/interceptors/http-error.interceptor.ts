/**
 * INTERCEPTOR HTTP
 * Maneja errores globales y añade logging
 */

import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse,
  HttpResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

@Injectable()
export class HttpErrorInterceptor implements HttpInterceptor {

  constructor() {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    
    console.log('🌐 HTTP Request:', request.method, request.url);
    
    const startTime = Date.now();
    
    return next.handle(request).pipe(
      tap(event => {
        if (event instanceof HttpResponse) {
          const duration = Date.now() - startTime;
          console.log(`✅ HTTP Response: ${event.status} (${duration}ms)`, event.body);
        }
      }),
      catchError((error: HttpErrorResponse) => {
        const duration = Date.now() - startTime;
        
        console.error('❌ HTTP Error:', {
          status: error.status,
          statusText: error.statusText,
          message: error.message,
          url: error.url,
          duration: `${duration}ms`
        });
        
        // Mensaje amigable según el error
        let userMessage = 'Ha ocurrido un error. Por favor, intenta de nuevo.';
        
        if (error.status === 0) {
          userMessage = 'No se puede conectar con el servidor. Verifica tu conexión o que el backend esté corriendo.';
        } else if (error.status === 400) {
          userMessage = 'Los datos enviados son incorrectos.';
        } else if (error.status === 404) {
          userMessage = 'El recurso solicitado no existe.';
        } else if (error.status === 500) {
          userMessage = 'Error interno del servidor.';
        } else if (error.status === 504) {
          userMessage = 'El servidor tardó demasiado en responder.';
        }
        
        // Mostrar notificación al usuario (puedes implementar un servicio de toast/snackbar)
        console.warn('💬 Mensaje para usuario:', userMessage);
        
        return throwError(() => error);
      })
    );
  }
}