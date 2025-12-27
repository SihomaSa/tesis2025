import { Routes } from '@angular/router';
import { authGuard, loginGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./components/home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'hero',
    loadComponent: () => import('./components/hero/hero.component').then(m => m.HeroComponent),
    canActivate: [loginGuard]
  },
  
  {
    path: 'analysis',
    loadComponent: () => import('./components/analysis/analysis.component').then(m => m.AnalysisComponent),
    canActivate: [authGuard]
  },
  {
    path: 'reports',
    loadComponent: () => import('./components/reports/reports.component').then(m => m.ReportsComponent),
    canActivate: [authGuard]
  },
  {
    path: '**',
    redirectTo: ''
  }
];