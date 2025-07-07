from django.core.management.base import BaseCommand
from gestion_transporte.models import DatasetTurnosIA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import joblib
import os

class Command(BaseCommand):
    help = 'Entrena un modelo IA para predecir asignación de turnos usando DatasetTurnosIA'

    def handle(self, *args, **options):
        self.stdout.write(" Cargando datos desde la base de datos...")
        datos = DatasetTurnosIA.objects.all().values(
            'disponible', 'estado_vehiculo', 'vehiculo_operativo', 'turno_asignado'
        )
        df = pd.DataFrame(list(datos))

        if df.empty:
            self.stdout.write(self.style.ERROR(" No hay datos en DatasetTurnosIA."))
            return

        self.stdout.write("Preprocesando datos...")
        df_encoded = pd.get_dummies(df, columns=['estado_vehiculo'])

        X = df_encoded.drop(columns=['turno_asignado'])
        y = df_encoded['turno_asignado']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.stdout.write("Entrenando modelo RandomForest...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        self.stdout.write("Evaluando modelo...")
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred)
        matriz = confusion_matrix(y_test, y_pred)

        self.stdout.write("Reporte de clasificación:")
        self.stdout.write(report)
        self.stdout.write("Matriz de confusión:")
        self.stdout.write(str(matriz))

        output_path = os.path.join("modelo_turnos.pkl")
        joblib.dump(model, output_path)

        self.stdout.write(self.style.SUCCESS(f"Modelo entrenado y guardado como {output_path}"))
