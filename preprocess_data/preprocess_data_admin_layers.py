import geopandas as gpd

# Pfad zu deiner .shp-Datei
shapefile_path = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Admin_layers\Assaba_Districts_layer.shp"

# Shapefile einlesen
gdf = gpd.read_file(shapefile_path)

# Zeige die ersten Einträge
print(gdf.head())

# Metadaten
print("CRS (Koordinatensystem):", gdf.crs)
print("Spalten:", gdf.columns)
print(gdf.transform)
print("Anzahl der Features:", len(gdf))


import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
gdf.plot(ax=ax, color="blue", edgecolor="black", alpha=0.5)
ax.set_title("Shapefile anzeigen")
plt.show()

print(gdf.columns)  # Zeigt alle Spalten (Attribute)
print(gdf.dtypes)  # Datentypen prüfen
print(gdf.iloc[0])  # Ein einzelnes Objekt ausgeben


print(gdf["FID_1"].unique())  # Alle Kategorien aus einer Spalte
