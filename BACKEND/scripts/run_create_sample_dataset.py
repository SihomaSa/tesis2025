# run_create_sample_dataset.py
import pandas as pd
import os

# Crear carpeta data si no existe
os.makedirs('data', exist_ok=True)

# Crear dataset de ejemplo
sample_data = {
    'comentario': [
        'Excelentes instalaciones en la universidad',
        'Los profesores son muy capacitados',
        'El servicio administrativo es lento',
        'La biblioteca tiene muchos libros',
        'El internet funciona muy bien',
        'Las aulas necesitan mantenimiento',
        'Buena enseñanza en las clases',
        'La atencion al alumno es deficiente',
        'Material bibliografico actualizado',
        'Sistema virtual muy practico'
    ],
    'sentimiento': [
        'Positivo', 'Positivo', 'Negativo', 'Positivo', 'Positivo',
        'Negativo', 'Positivo', 'Negativo', 'Positivo', 'Positivo'
    ]
}

df = pd.DataFrame(sample_data)
df.to_csv('data/dataset_instagram_unmsm.csv', index=False)
print("Dataset de ejemplo creado en data/dataset_instagram_unmsm.csv")
print(f"Total de registros: {len(df)}")