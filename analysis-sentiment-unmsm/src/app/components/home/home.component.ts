// import { Component } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { NavbarComponent } from '../../components/navbar/navbar.component';
// import { HeroComponent } from '../../components/hero/hero.component';
// import { FooterComponent } from '../../components/footer/footer.component';

// @Component({
//   selector: 'app-home',
//   standalone: true,
//   imports: [
//     CommonModule,
//     NavbarComponent,
//     HeroComponent,
//     FooterComponent
//   ],
//   template: `
//      export class HomeComponent {}
// app.component.ts
//   `,
//   styles: []
// })
// export class HomeComponent {}

// import { Component } from '@angular/core';
// import { NavbarComponent } from '../../components/navbar/navbar.component';
// import { HeroComponent } from '../../components/hero/hero.component';
// import { AnalysisComponent } from '../../components/analysis/analysis.component';
// import { ReportsComponent } from '../../components/reports/reports.component';
// import { FooterComponent } from '../../components/footer/footer.component';

// @Component({
//   selector: 'app-home',
//   standalone: true,
//   imports: [
//     NavbarComponent, 
//     HeroComponent, 
//     AnalysisComponent,
//     ReportsComponent,
//     FooterComponent
//   ],
//   template: `
//     <div class="dashboard-container">
//       <app-navbar 
//         >
//       </app-navbar>
      
//       <app-hero></app-hero>
//       <app-analysis *ngIf="currentView === 'analysis'"></app-analysis>
//       <app-reports *ngIf="currentView === 'reports'"></app-reports>
      
//       <app-footer></app-footer>
//     </div>
//   `,
//   styles: [`
//     .dashboard-container {
//       min-height: 100vh;
//       background: linear-gradient(to bottom right, #f9fafb, #e5e7eb);
//     }
//   `]
// })
//  export class HomeComponent {}
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../../components/navbar/navbar.component';
import { HeroComponent } from '../../components/hero/hero.component';
import { AnalysisComponent } from '../../components/analysis/analysis.component';
import { ReportsComponent } from '../../components/reports/reports.component';
import { FooterComponent } from '../../components/footer/footer.component';

// Definir el mismo tipo aquí también para consistencia
type ViewType = 'dashboard' | 'analysis' | 'reports';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    NavbarComponent, 
    HeroComponent, 
    AnalysisComponent,
    ReportsComponent,
    FooterComponent
  ],
  template: `
    <div class="dashboard-container">
      <app-navbar 
        [activeView]="currentView"
        (viewChange)="onViewChange($event)">
      </app-navbar>
      
      <!-- Vista Dashboard/Hero -->
      <app-hero *ngIf="currentView === 'dashboard'"></app-hero>
      
      <!-- Vista Analysis -->
      <app-analysis *ngIf="currentView === 'analysis'"></app-analysis>
      
      <!-- Vista Reports -->
      <app-reports *ngIf="currentView === 'reports'"></app-reports>
      
      <app-footer></app-footer>
    </div>
  `,
  styles: [`
    .dashboard-container {
      min-height: 100vh;
      background: linear-gradient(to bottom right, #f9fafb, #e5e7eb);
    }
  `]
})
export class HomeComponent {
  currentView: ViewType = 'dashboard';

  onViewChange(view: ViewType) {
    this.currentView = view;
  }
}