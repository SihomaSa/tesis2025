/**
 * SERVICIO DE AUTENTICACIÓN
 * Maneja autenticación con Firebase
 */

import { Injectable, inject } from '@angular/core';
import { Router } from '@angular/router';
import { 
  Auth, 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User,
  UserCredential
} from '@angular/fire/auth';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private auth = inject(Auth);
  private router = inject(Router);
  
  // Observable del usuario actual
  private userSubject = new BehaviorSubject<User | null>(null);
  public user$: Observable<User | null> = this.userSubject.asObservable();
  
  // Estado de autenticación
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor() {
    console.log('🔐 AuthService inicializado');
    this.initAuthListener();
  }

  /**
   * Inicializar listener de autenticación
   */
  private initAuthListener(): void {
    onAuthStateChanged(this.auth, (user) => {
      console.log('👤 Estado de autenticación cambió:', user?.email || 'No autenticado');
      this.userSubject.next(user);
      this.isAuthenticatedSubject.next(!!user);
      
      // Guardar datos básicos en localStorage
      if (user) {
        localStorage.setItem('user_email', user.email || '');
        localStorage.setItem('user_name', user.displayName || user.email?.split('@')[0] || 'Usuario');
        localStorage.setItem('user_photo', user.photoURL || '');
      } else {
        localStorage.removeItem('user_email');
        localStorage.removeItem('user_name');
        localStorage.removeItem('user_photo');
      }
    });
  }

  /**
   * Iniciar sesión con email y contraseña
   */
  async login(email: string, password: string): Promise<UserCredential> {
    try {
      console.log('🔐 Intentando login:', email);
      const credential = await signInWithEmailAndPassword(this.auth, email, password);
      console.log('✅ Login exitoso:', credential.user.email);
      await this.router.navigate(['/dashboard']);
      return credential;
    } catch (error: any) {
      console.error('❌ Error en login:', error);
      throw this.handleAuthError(error);
    }
  }

  /**
   * Registrar nuevo usuario
   */
  async register(email: string, password: string): Promise<UserCredential> {
    try {
      console.log('📝 Registrando usuario:', email);
      const credential = await createUserWithEmailAndPassword(this.auth, email, password);
      console.log('✅ Registro exitoso:', credential.user.email);
      await this.router.navigate(['/dashboard']);
      return credential;
    } catch (error: any) {
      console.error('❌ Error en registro:', error);
      throw this.handleAuthError(error);
    }
  }

  /**
   * Cerrar sesión
   */
  async logout(): Promise<void> {
    try {
      console.log('👋 Cerrando sesión...');
      await signOut(this.auth);
      console.log('✅ Sesión cerrada');
      await this.router.navigate(['/login']);
    } catch (error) {
      console.error('❌ Error cerrando sesión:', error);
      throw error;
    }
  }

  /**
   * Obtener usuario actual
   */
  getCurrentUser(): User | null {
    return this.userSubject.value;
  }

  /**
   * Verificar si está autenticado
   */
  isAuthenticated(): boolean {
    return this.isAuthenticatedSubject.value;
  }

  /**
   * Obtener nombre del usuario
   */
  getUserName(): string {
    const user = this.getCurrentUser();
    return user?.displayName || 
           user?.email?.split('@')[0] || 
           localStorage.getItem('user_name') || 
           'Usuario';
  }

  /**
   * Obtener email del usuario
   */
  getUserEmail(): string {
    const user = this.getCurrentUser();
    return user?.email || 
           localStorage.getItem('user_email') || 
           '';
  }

  /**
   * Obtener foto del usuario
   */
  getUserPhoto(): string {
    const user = this.getCurrentUser();
    return user?.photoURL || 
           localStorage.getItem('user_photo') || 
           'assets/default-avatar.png';
  }

  /**
   * Obtener UID del usuario
   */
  getUserId(): string {
    return this.getCurrentUser()?.uid || '';
  }

  /**
   * Manejo de errores de autenticación
   */
  private handleAuthError(error: any): Error {
    let message = 'Error de autenticación';
    
    switch (error.code) {
      case 'auth/invalid-email':
        message = 'Email inválido';
        break;
      case 'auth/user-disabled':
        message = 'Usuario deshabilitado';
        break;
      case 'auth/user-not-found':
        message = 'Usuario no encontrado';
        break;
      case 'auth/wrong-password':
        message = 'Contraseña incorrecta';
        break;
      case 'auth/email-already-in-use':
        message = 'El email ya está registrado';
        break;
      case 'auth/weak-password':
        message = 'La contraseña es muy débil';
        break;
      case 'auth/network-request-failed':
        message = 'Error de red. Verifica tu conexión';
        break;
      case 'auth/too-many-requests':
        message = 'Demasiados intentos. Intenta más tarde';
        break;
      default:
        message = error.message || 'Error desconocido';
    }
    
    return new Error(message);
  }
}