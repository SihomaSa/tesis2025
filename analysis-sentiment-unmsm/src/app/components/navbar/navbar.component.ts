import { Component, Output, EventEmitter, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

// Definir tipo para las vistas
type ViewType = 'dashboard' | 'analysis' | 'reports';

interface NavItem {
  id: ViewType;
  label: string;
  icon: string;
}

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  template: `
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <div class="logo-container">
            <span class="logo-icon">🎓</span>
          </div>
          <div class="header-info">
            <h1>UNMSM - Dashboard de Análisis de Sentimientos</h1>
            <p>Predicción de Satisfacción de Usuarios en Instagram</p>
          </div>
        </div>
        <div class="header-right">
          <p class="header-title">Investigación de Maestría</p>
          <p class="header-date">Actualizado: {{ getCurrentDate() }}</p>
        </div>
      </div>
    </header>

    <nav class="dashboard-nav">
      <div class="nav-content">
        <button 
          *ngFor="let item of navItems"
          [class.active]="activeView === item.id"
          (click)="onNavigate(item.id)"
          class="nav-button">
          <span class="nav-icon">{{ item.icon }}</span>
          {{ item.label }}
        </button>
      </div>
    </nav>
  `,
  styles: [`
    .dashboard-header {
      background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
      color: white;
      padding: 1.5rem 2rem;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1200px;
      margin: 0 auto;
    }
    .header-left {
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .logo-container {
      background: rgba(255, 255, 255, 0.2);
      padding: 0.75rem;
      border-radius: 12px;
      backdrop-filter: blur(10px);
    }
    .logo-icon {
      font-size: 2rem;
    }
    .header-info h1 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 700;
    }
    .header-info p {
      margin: 0.25rem 0 0 0;
      opacity: 0.9;
      font-size: 0.9rem;
    }
    .header-right {
      text-align: right;
    }
    .header-title {
      margin: 0;
      font-weight: 600;
      font-size: 0.9rem;
    }
    .header-date {
      margin: 0.25rem 0 0 0;
      opacity: 0.8;
      font-size: 0.8rem;
    }
    .dashboard-nav {
      background: white;
      border-bottom: 1px solid #e5e7eb;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .nav-content {
      display: flex;
      gap: 0.5rem;
      padding: 1rem 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }
    .nav-button {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.75rem 1.5rem;
      border: 2px solid transparent;
      background: transparent;
      color: #6b7280;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;
      font-weight: 500;
    }
    .nav-button:hover {
      background: #f3f4f6;
      color: #374151;
    }
    .nav-button.active {
      background: #3b82f6;
      color: white;
      border-color: #3b82f6;
    }
    .nav-icon {
      font-size: 1.1rem;
    }
  `]
})
export class NavbarComponent {
  @Input() activeView: ViewType = 'dashboard';
  @Output() viewChange = new EventEmitter<ViewType>();

  navItems: NavItem[] = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'analysis', label: 'Análisis Individual', icon: '🔍' },
    { id: 'reports', label: 'Reportes', icon: '📋' }
  ];

  getCurrentDate(): string {
    return new Date().toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  onNavigate(view: ViewType) {
    this.viewChange.emit(view);
  }
}