import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import glob
import ast 

# 📌 1. Daten laden
data = pd.read_csv("combined_joined_data.csv")  # Deine CSV mit den 1200 Datenpunkten und ihren Werten
data['Year'] = data['Year'].astype(int)
model_classification = RandomForestRegressor()

# 📌 2. Funktion zum Trainieren und Vorhersagen für einen einzelnen Punkt im Bezirk
def train_predict_for_district(data, district_id):
    # Extrahiere alle Punkte des aktuellen Bezirks (District) basierend auf der FID_1 (district_id)
    district_data = data[data['FID_1'] == district_id]
    
    if len(district_data) == 0:
        return None, None, None
    print(len(district_data))
    all_predictions = []  # Liste für alle Vorhersagen eines Bezirks
    model_precipitation = RandomForestRegressor()
    model_population = RandomForestRegressor()
    model_absorption = RandomForestRegressor()
    X_train_precipitation = []
    X_train_absorption = []
    X_train_population = []
    y_precipitation = []
    y_absorption = []
    y_population = []
    columns = ["FID_1", "Longitude", "Latitude", "Precipitation", "Population", "Absorption", "Classification"]
    df = pd.DataFrame(columns=columns)
    # Iteriere über alle Datenpunkte im Bezirk
    for _, point_data in district_data.iterrows():
        lat, lon = point_data['Latitude'], point_data['Longitude']
        
        # Filtere Daten für den aktuellen Punkt und 2010-2022
        point_train_data = district_data[(district_data['Latitude'] == lat) & (district_data['Longitude'] == lon) & (district_data['Year'] <= 2022)]
        
        # Feature: Jahr, Zielvariablen: Population, Absorption, Precipitation
        X_train_precipitation.append(point_train_data['Precipitation'])
        X_train_absorption.append(point_train_data['Precipitation'])
        X_train_population.append(point_train_data['Precipitation'])

        # Testdaten für 2020-2023 (Vergleich mit echten Werten)
        point_test_data = district_data[(district_data['Latitude'] == lat) & (district_data['Longitude'] == lon) & (district_data['Year'] > 2022)]
        #y_precipitation.append(point_train_data['Population'])
        y_absorption.append(point_test_data['Absorption'])
        y_population.append(point_test_data['Population'])
        y_precipitation.append(point_test_data['Precipitation'])
        X_test = point_test_data[['Year']]

        # Trainiere Modelle für Population, Absorption und Precipitation
    point_train_data = district_data[(district_data['Latitude'] == lat) & (district_data['Longitude'] == lon) & (district_data['Year'] <= 2023 )& (district_data['Year'] > 2010)]
    model_population.fit(X_train_precipitation, y_precipitation)
    print(y_precipitation)
    print([point_train_data['Precipitation']])
    print(model_population.predict([point_train_data['Precipitation']]))
    model_absorption.fit(X_train_absorption, y_absorption)
        
    model_precipitation.fit(X_train_population, y_population)
    for _, point_data in district_data.iterrows():
        lat, lon = point_data['Latitude'], point_data['Longitude']
        point_eval_data = district_data[(district_data['Latitude'] == lat) & (district_data['Longitude'] == lon) & (district_data['Year'] <= 2023 )& (district_data['Year'] > 2010)]
        precip_predict = model_precipitation.predict([point_eval_data['Precipitation']])
        popul_predict = model_population.predict([point_eval_data['Population']])
        absorp_predict = model_absorption.predict([point_eval_data['Absorption']])
        new_entry = {
            "FID_1": district_id,
            "Longitude": lat,
            "Latitude": lon,
            "Precipitation": precip_predict,
            "Population": popul_predict,
            "Absorption": absorp_predict,
            "Classification": 0
        }

        # Füge den neuen Eintrag hinzu
        df = df._append(new_entry, ignore_index=True)

    df.to_csv(f"{district_id}.csv", index=False)
    return
        # Vorhersagen für 2020-2023
    population_pred = model_population.predict(X_test)
    absorption_pred = model_absorption.predict(X_test)
    precipitation_pred = model_precipitation.predict(X_test)
        
        # Füge Vorhersagen für diesen Punkt zur Liste der Vorhersagen hinzu
    all_predictions.append({
            'FID_1': district_id,
            'Latitude': lat,
            'Longitude': lon,
            'Population_2023': population_pred[-1],  # Vorhersage für 2023
            'Absorption_2023': absorption_pred[-1],  # Vorhersage für 2023
            'Precipitation_2023': precipitation_pred[-1]  # Vorhersage für 2023
    })

        # Nun trainiere erneut mit den echten Werten für 2023 und mache eine Vorhersage für 2024
        # Hinzufügen der tatsächlichen 2023-Werte für Supervision
    actual_2023_population = point_test_data['Population'].values[-1]
    actual_2023_absorption = point_test_data['Absorption'].values[-1]
    actual_2023_precipitation = point_test_data['Precipitation'].values[-1]
        
        # Vorhersage für 2024
    population_2024 = model_population.predict([[2024]])
    absorption_2024 = model_absorption.predict([[2024]])
    precipitation_2024 = model_precipitation.predict([[2024]])

        # Speichern der Vorhersagen für 2024
    all_predictions[-1].update({
            'Population_2024': population_2024[0],
            'Absorption_2024': absorption_2024[0],
            'Precipitation_2024': precipitation_2024[0]
    })

    return all_predictions

# 📌 3. Alle Bezirke durchgehen und Vorhersagen für jeden Bezirk machen
all_predictions = []

# Gehe über alle Bezirke, z.B. von FID_1 = 67 bis 93
for district_id in range(67, 91):
    print(f"Trainiere Modell für Bezirk {district_id}...")
    break
    # Trainiere und teste das Modell für den aktuellen Bezirk
    try:
        predictions = train_predict_for_district(data, district_id)
    except:
        break

path = r"C://Users//paulb//PycharmProjects//start_hack_25_data//predicted_data//"  # Passe den Pfad zum Verzeichnis mit deinen CSV-Dateien an

# Alle CSV-Dateien im Verzeichnis finden
csv_files = glob.glob(path + "*.csv")

# Eine leere Liste, um die DataFrames zu speichern
dfs = []

# Alle CSV-Dateien einlesen und zur Liste hinzufügen
for file in csv_files:
    df = pd.read_csv(file)  # Lese jede CSV-Datei
    dfs.append(df)  # Füge das DataFrame der Liste hinzu

# Alle DataFrames in der Liste zu einem einzigen DataFrame zusammenführen
merged_df = pd.concat(dfs, ignore_index=True)

# Speichern des zusammengeführten DataFrames als eine CSV-Datei
merged_df.to_csv("merged_data.csv", index=False)    

X_train_classification = []
y_classification = []
for _, point_data in data.iterrows():
    lat, lon = point_data['Latitude'], point_data['Longitude']
    X_train_classification.append([point_data['Precipitation'], point_data["Population"], point_data["Absorption"]])
    y_classification.append(point_data["Classification"])
    

model_classification.fit(X_train_classification, y_classification)

# 📌 1. Lade die zusammengeführte CSV-Datei
df = pd.read_csv("merged_data.csv")

# 📌 2. Iteriere durch jeden Eintrag und ändere eine Spalte
for index, row in df.iterrows():
    classification_predict = model_classification.predict([[ast.literal_eval(row["Precipitation"])[0], ast.literal_eval(row["Population"])[0], ast.literal_eval(row["Absorption"])[0]]])
    df.at[index, 'Classification'] = classification_predict

df.to_csv("modified_merged_data.csv", index=False)
