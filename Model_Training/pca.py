import pandas as pd
from sklearn.preprocessing import StandardScaler

# Lade die CSV-Datei
df = pd.read_csv('joined_data_2010.csv')

# Selektiere nur die relevanten Spalten
features = ['Population', 'Absorption', 'Precipitation', 'Classification']  # Füge hier alle relevanten Spalten hinzu
X = df[features].dropna()  # Entferne fehlende Werte

# Normiere die Daten (wichtig für PCA)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

from sklearn.decomposition import PCA

# PCA mit 2 Hauptkomponenten
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X_scaled)

# PCA-Ergebnisse in einen DataFrame umwandeln
principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# Füge die Classification-Spalte hinzu
principal_df['Classification'] = df['Classification']

# Ergebnisse anschauen
print(principal_df.head())
# Erklärte Varianz pro Hauptkomponente
print(f"Erklärte Varianz durch PC1: {pca.explained_variance_ratio_[0]}")
print(f"Erklärte Varianz durch PC2: {pca.explained_variance_ratio_[1]}")

# PCA-Komponenten (Ladungen) anzeigen
print("PCA Komponenten (Ladungen):")
print(pca.components_)

# Visualisiere die Ladungen der Merkmale auf den Komponenten
import matplotlib.pyplot as plt
import numpy as np

labels = features[:-1]  # Entferne die 'Classification' Spalte

# Korrelation zwischen den PCs und der Klassifikation
correlation_pc_class = principal_df[['PC1', 'PC2', 'Classification']].corr()
print("Korrelationsmatrix zwischen PCs und Classification:")
print(correlation_pc_class)

from sklearn.ensemble import RandomForestRegressor

# Trainingsdaten und Zielvariable definieren
X = df[['Population', 'Absorption', 'Precipitation']]  # Merkmale
y = df['Classification']  # Zielvariable
print(X.shape)  # Form von X, sollte (n_samples, n_features) sein
print(y.shape)  # Form von y, sollte (n_samples,) sein

# Random Forest Modell erstellen
model = RandomForestRegressor()
model.fit(X, y)

# Feature Importances
importances = model.feature_importances_
plt.bar(X.columns, importances)
plt.title('Feature Importances (Random Forest)')
plt.xlabel('Merkmale')
plt.ylabel('Wichtigkeit')
plt.show()


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Deine Features (z.B. Population, Absorption, Precipitation)
X = all_points_df[['Population', 'Absorption', 'Precipitation']]  # Features

# Zielwert: Classification (die du vorhersagen willst)
y = all_points_df['Classification']

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Regressor initialisieren
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

# Modell trainieren
rf_regressor.fit(X_train, y_train)

# Modellbewertung auf Testdaten
y_pred = rf_regressor.predict(X_test)

# Metriken anzeigen
print(f"MAE: {mean_absolute_error(y_test, y_pred)}")


# Beispieldaten für zukünftige Jahre (z.B. 2024)
future_data = pd.DataFrame({
    'Population': [estimated_population_2024],  # Schätzungen für 2024
    'Absorption': [estimated_absorption_2024],  # Schätzungen für 2024
    'Precipitation': [estimated_precipitation_2024]  # Schätzungen für 2024
})

# Vorhersagen für die zukünftigen Jahre machen
future_predictions = rf_regressor.predict(future_data)

print(f"Vorhersagte Classification für 2024: {future_predictions[0]}")
import matplotlib.pyplot as plt

# Angenommen, du hast eine Liste von zukünftigen Jahren und deren Vorhersagen:
years = [2024, 2025, 2026]
predictions = [rf_regressor.predict(pd.DataFrame({'Population': [pop], 'Absorption': [abs], 'Precipitation': [precip]}))[0] for pop, abs, precip in zip(future_populations, future_absorptions, future_precipitations)]

# Visualisierung
plt.plot(years, predictions, marker='o')
plt.xlabel('Jahre')
plt.ylabel('Vorhergesagte Classification')
plt.title('Prognose der Classification über die Jahre')
plt.show()

# Angenommene Features nach PCA (PC1, PC2, PC3, ...)
X_pca = pca.transform(X)  # Daten nach PCA-Transformation

# Trainiere den RandomForest mit den PCs
rf_regressor.fit(X_pca, y)

# Für zukünftige Daten nach PCA transformieren und dann vorhersagen
future_pca_data = pca.transform(future_data)
future_predictions_pca = rf_regressor.predict(future_pca_data)

print(f"Vorhersagte Classification für 2024 mit PCA: {future_predictions_pca[0]}")


#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Angenommene Daten: DataFrame mit den historischen Daten für ein Jahr (Jahr als Feature)
historical_data = pd.read_csv("combined_joined_data.csv")  # Dein Datensatz mit mehreren Jahren

# Jedes Jahr als Feature und die entsprechenden Population/Absorption/Precipitation als Ziel
X = historical_data['Year'].values.reshape(-1, 1)  # Jahr als Feature
y_population = historical_data['Population'].values  # Zielvariable Population

# Trainiere ein lineares Regressionsmodell
model_population = LinearRegression()
model_population.fit(X, y_population)

# Vorhersage für zukünftige Jahre (z.B. 2024, 2025, 2026)
future_years = np.array([2024, 2025, 2026]).reshape(-1, 1)
future_population_predictions = model_population.predict(future_years)

# Zeige die Vorhersagen an
for year, prediction in zip(future_years, future_population_predictions):
    print(f"Vorhergesagte Population für {year[0]}: {prediction}")

# Visualisierung der historischen Daten und der Vorhersage
plt.scatter(X, y_population, color='blue')  # Historische Daten
plt.plot(future_years, future_population_predictions, color='red', label='Vorhersage')
plt.xlabel("Jahr")
plt.ylabel("Population")
plt.title("Vorhersage der Population")
plt.legend()
plt.show()

from sklearn.preprocessing import PolynomialFeatures

# Polynomial Regression (z.B. Grad 2)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)  # Transformation der Jahre in polynomiale Features

# Trainiere ein polynomiales Regressionsmodell
model_population_poly = LinearRegression()
model_population_poly.fit(X_poly, y_population)

# Vorhersage für zukünftige Jahre
future_X_poly = poly.transform(future_years)
future_population_predictions_poly = model_population_poly.predict(future_X_poly)

# Zeige die Vorhersagen an
for year, prediction in zip(future_years, future_population_predictions_poly):
    print(f"Vorhergesagte Population für {year[0]} (polynomiale Regression): {prediction}")

from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Zeitreihe für Population erstellen (Jahr als Index)
historical_data.set_index('Year', inplace=True)
population_series = historical_data['Population']

# ARIMA-Modell anpassen (1,1,1: Ar, I, MA)
model = ARIMA(population_series, order=(1, 1, 1))
model_fit = model.fit()

# Vorhersage für zukünftige Jahre
forecast = model_fit.forecast(steps=3)  # z.B. 3 Jahre in die Zukunft (2024, 2025, 2026)

# Visualisierung der Vorhersage
plt.plot(population_series, color='blue', label='Historische Daten')
plt.plot([2024, 2025, 2026], forecast, color='red', label='Vorhersage')
plt.xlabel("Jahr")
plt.ylabel("Population")
plt.title("ARIMA Vorhersage der Population")
plt.legend()
plt.show()

# Ausgabe der Vorhersagen
for year, prediction in zip([2024, 2025, 2026], forecast):
    print(f"Vorhergesagte Population für {year}: {prediction}")


# %%
import pandas as pd
import os

# Verzeichnis, in dem sich deine CSV-Dateien befinden
data_dir = r"C:\Users\paulb\PycharmProjects\start_hack_25_data"

# Liste aller CSV-Dateien im Verzeichnis
file_names = [f for f in os.listdir(data_dir) if f.startswith("joined_data_") and f.endswith(".csv")]

# Leere Liste für DataFrames
dfs = []

# Durch alle Dateien iterieren und die Daten in eine Liste laden
for file_name in file_names:
    file_path = os.path.join(data_dir, file_name)
    
    # Extrahiere das Jahr aus dem Dateinamen
    year = int(file_name.split('_')[2].split('.')[0])  # "joined_data_2010.csv" -> Jahr 2010
    
    df = pd.read_csv(file_path)
    
    # Füge eine neue Spalte "Year" hinzu, die das Jahr speichert
    df['Year'] = year
    
    # Füge den DataFrame der Liste hinzu
    dfs.append(df)

# Alle DataFrames in der Liste zu einem einzigen DataFrame zusammenführen
combined_df = pd.concat(dfs, ignore_index=True)

# Optional: Speichern des kombinierten DataFrames als neue CSV-Datei
combined_df.to_csv(os.path.join(data_dir, "combined_joined_data.csv"), index=False)

# Ausgabe des kombinierten DataFrames (erste 5 Zeilen)
print(combined_df.head())


#%%
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

print(historical_data)
# Daten vorbereiten
#X = historical_data['Year'].values.reshape(-1, 1)  # Jahr als Feature
y = historical_data['Population'].values  # Zielvariable

# Polynomial Features erstellen (z.B. Grad 2)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Polynomiale Regression
model = LinearRegression()
model.fit(X_poly, y)

# Vorhersage für zukünftige Jahre
future_years = np.array([2024, 2025, 2026]).reshape(-1, 1)
future_years_poly = poly.transform(future_years)
predictions = model.predict(future_years_poly)

# Visualisierung der Vorhersage
plt.scatter(X, y, color='blue', label='Historische Daten')
plt.plot(future_years, predictions, color='red', label='Vorhersage')
plt.xlabel("Jahr")
plt.ylabel("Population")
plt.title("Polynomiale Vorhersage der Population")
plt.legend()
plt.show()

# Ausgabe der Vorhersagen
for year, prediction in zip(future_years, predictions):
    print(f"Vorhergesagte Population für {year[0]}: {prediction}")


# %%
