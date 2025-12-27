import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap, finalize } from 'rxjs/operators';

@Injectable()
export class LoadingInterceptor implements HttpInterceptor {
  private totalRequests = 0;

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    console.log('🌐 Request iniciado:', req.url);
    this.totalRequests++;

    const started = Date.now();

    return next.handle(req).pipe(
      tap({
        next: (event) => {
          if (event instanceof HttpResponse) {
            const elapsed = Date.now() - started;
            console.log(`✅ Response recibido en ${elapsed}ms:`, req.url);
          }
        },
        error: (error) => {
          const elapsed = Date.now() - started;
          console.error(`❌ Error después de ${elapsed}ms:`, req.url, error);
        }
      }),
      finalize(() => {
        this.totalRequests--;
        console.log(`📊 Requests activos: ${this.totalRequests}`);
      })
    );
  }
}