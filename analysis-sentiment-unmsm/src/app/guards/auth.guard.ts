import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../core/services/auth.service';  // ✅ Ruta corregida
import { map, take } from 'rxjs/operators';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  return authService.user$.pipe(
    take(1),
    map(user => {
      if (user) {
        console.log('✅ Usuario autenticado:', user.email);
        return true;
      } else {
        console.log('❌ Usuario no autenticado, redirigiendo a login');
        router.navigate(['/login']);
        return false;
      }
    })
  );
};

export const loginGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  return authService.user$.pipe(
    take(1),
    map(user => {
      if (user) {
        console.log('✅ Usuario ya autenticado, redirigiendo a dashboard');
        router.navigate(['/dashboard']);
        return false;
      } else {
        console.log('✅ Usuario no autenticado, permitiendo acceso a login');
        return true;
      }
    })
  );
};