import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, NavigationEnd } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';  // ✅ Ruta corregida
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit {
  private authService = inject(AuthService);
  private router = inject(Router);
  
  userName: string = '';
  userEmail: string = '';
  userPhoto: string = '';
  currentRoute: string = '';

  ngOnInit(): void {
    this.loadUserData();
    this.updateActiveRoute();
    
    // Suscribirse a cambios de ruta
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        this.updateActiveRoute();
      });
  }

  updateActiveRoute(): void {
    this.currentRoute = this.router.url;
  }

  isActive(route: string): boolean {
    return this.currentRoute.includes(route);
  }

  loadUserData(): void {
    this.userName = this.authService.getUserName();
    this.userEmail = this.authService.getUserEmail();
    this.userPhoto = this.authService.getUserPhoto();
  }

  async logout(): Promise<void> {
    try {
      await this.authService.logout();
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
      alert('Error al cerrar sesión');
    }
  }
}