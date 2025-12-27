import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface KPI {
  icon: string;
  label: string;
  value: string;
  sublabel: string;
  type?: string;
}

interface Prediction {
  icon: string;
  title: string;
  value: string;
  label: string;
  valueClass: string;
  type?: string;
}

interface Metric {
  icon: string;
  label: string;
  value: string;
}

@Component({
  selector: 'app-indicadores',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './indicadores.component.html',
  styleUrls: ['./indicadores.component.scss']
})
export class IndicadoresComponent implements OnInit {
  currentDate: string = '';

  kpis: KPI[] = [
    {
      icon: '📦',
      label: 'Total de Registros',
      value: '45,892',
      sublabel: 'Datos de producción analizados',
      type: ''
    },
    {
      icon: '⚠️',
      label: 'Anomalías Detectadas',
      value: '1,847',
      sublabel: 'Precios fuera de lo normal',
      type: 'alert'
    },
    {
      icon: '📍',
      label: 'Zona de Mayor Producción',
      value: 'Valle del Chira',
      sublabel: 'Región destacada',
      type: ''
    },
    {
      icon: '🌾',
      label: 'Cultivo Principal',
      value: 'Arroz',
      sublabel: 'Mayor volumen de producción',
      type: ''
    },
    {
      icon: '📉',
      label: 'Variación de Precios',
      value: '-2.34%',
      sublabel: 'Respecto al mes anterior',
      type: 'negative'
    }
  ];

  predictions: Prediction[] = [
    {
      icon: '💰',
      title: 'Precio Predicho',
      value: 'S/1.39',
      label: 'por kg',
      valueClass: 'price-predicted',
      type: ''
    },
    {
      icon: '📊',
      title: 'Precio Promedio',
      value: 'S/0.47',
      label: 'Histórico regional',
      valueClass: 'price-average',
      type: ''
    },
    {
      icon: '✅',
      title: 'Riesgo de Escasez',
      value: 'BAJO RIESGO',
      label: 'Condiciones favorables',
      valueClass: 'risk-level',
      type: 'success'
    }
  ];

  metrics: Metric[] = [
    {
      icon: '🌾',
      label: 'Hectáreas Sembradas',
      value: '100 ha'
    },
    {
      icon: '🌱',
      label: 'Hectáreas Cosechadas',
      value: '95 ha'
    },
    {
      icon: '📦',
      label: 'Producción Total',
      value: '5,000 toneladas'
    },
    {
      icon: '📅',
      label: 'Período',
      value: 'Enero 2024'
    }
  ];

  ngOnInit(): void {
    this.setCurrentDate();
  }

  setCurrentDate(): void {
    const date = new Date();
    const options: Intl.DateTimeFormatOptions = { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    };
    this.currentDate = date.toLocaleDateString('es-ES', options);
    // Capitalizar primera letra
    this.currentDate = this.currentDate.charAt(0).toUpperCase() + this.currentDate.slice(1);
  }
}
