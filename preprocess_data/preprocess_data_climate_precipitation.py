import rasterio
import matplotlib.pyplot as plt
import numpy as np#
from matplotlib import pyplot
import pandas as pd
import fiona
import shapefile  # Required for reading .dbf
import geopandas as gpd
import rasterio
import rasterio.features
import rasterio.warp

tif_file = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Climate_Precipitation_Data\2015R.tif"

import rasterio
from rasterio.plot import show
import rasterio
import numpy as np
import matplotlib.pyplot as plt

with rasterio.open(tif_file) as dataset:
    print("Metadaten:", dataset.meta)
    print("CRS:", dataset.crs)  # Prüft, ob das CRS erkannt wurde
    print("Transform:", dataset.transform)  
    band1 = dataset.read(1)  # Erstes Band
    nodata = dataset.nodata  # NoData-Wert auslesen
    transform = dataset.transform
    print("Skalierungsfaktor:", dataset.scales) 
    height, width = band1.shape

    show(dataset)
# Liste für Punkte
raster_points = []

for row in range(height):
    for col in range(width):
        lon, lat = dataset.xy(row, col)  # Geokoordinaten berechnen
        value = band1[row, col]  # Pixelwert
        if value != dataset.nodata:  # NoData ignorieren
            raster_points.append((lon, lat, value))


shapefile_path = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Admin_layers\Assaba_Districts_layer.shp"
regions_gdf = gpd.read_file(shapefile_path)

# Als DataFrame speichern

raster_df = pd.DataFrame(raster_points, columns=["Longitude", "Latitude", "Precipitation"])

# In GeoDataFrame konvertieren
raster_gdf = gpd.GeoDataFrame(raster_df, geometry=gpd.points_from_xy(raster_df.Longitude, raster_df.Latitude), crs="EPSG:4326")
#

# Spatial Join zwischen Punkten (Raster) und Regionen (Polygone)
joined_gdf = gpd.sjoin(raster_gdf, regions_gdf, how="inner", predicate="within")
# Durchschnittlichen und maximalen Niederschlag pro Polygon berechnen
precip_stats = joined_gdf.groupby("FID_1")["Precipitation"].agg(["mean", "max"]).reset_index()

# Ausgabe der Statistik
print(precip_stats.head())

# Mit dem originalen Regionen-Shapefile verknüpfen
regions_gdf = regions_gdf.merge(precip_stats, on="FID_1")

# Ergebnis anzeigen
print(regions_gdf[["FID_1", "mean", "max"]])

import matplotlib.pyplot as plt

# Plot mit Niederschlag pro Region
fig, ax = plt.subplots(figsize=(10, 8))
regions_gdf.plot(column="mean", cmap="Blues", edgecolor="black", legend=True, ax=ax)
ax.set_title("Durchschnittlicher Niederschlag pro Region (2010)")
plt.show()

# Open a file for writing (will create it if it doesn't exist)
with open("output.txt", "w") as file:
    file.write(str(joined_gdf))

print("Text has been written to output.txt")
quit()
# Open a file for writing (will create it if it doesn't exist)
with open("output.txt", "w") as file:
    file.write(str(raster_gdf))

print("Text has been written to output.txt")


quit()
# q-Werte mit NaN ersetzen
band1 = np.where(band1 == nodata, np.nan, band1)

# Define the string to write
text_to_write = str(np.array(band1))
np.savetxt('array_data.txt', np.array(band1), fmt='%.6f')

plt.hist(band1[~np.isnan(band1)].flatten(), bins=50, color="blue", alpha=0.7)
plt.xlabel("Pixelwerte")
plt.ylabel("Anzahl der Pixel")
plt.title("Histogramm der Rasterwerte")
plt.show()
# Min & Max Werte im Raster prüfen
print(np.unique(band1))  # Gibt dir eine Liste aller Werte

print("Min. Wert:", np.nanmin(band1))
print("Max. Wert:", np.nanmax(band1))

# Raster mit NoData-Maske plotten
plt.figure(figsize=(6, 8))
plt.imshow(band1, cmap="viridis", interpolation="nearest")
plt.colorbar(label="Pixelwerte")
plt.title("Rasterdaten ohne NoData-Werte")
plt.show()

quit()