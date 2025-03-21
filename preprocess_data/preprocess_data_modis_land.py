import rasterio
import matplotlib.pyplot as plt
import numpy as np#
from matplotlib import pyplot
import pandas as pd
import fiona
import shapefile  # Required for reading .dbf

import rasterio
import rasterio.features
import rasterio.warp

tif_file = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Modis_Land_Cover_Data\2010LCT.tif"

import rasterio
from rasterio.plot import show
import rasterio
import numpy as np
import matplotlib.pyplot as plt

with rasterio.open(tif_file) as dataset:
    band1 = dataset.read(1)  # Erstes Band
    nodata = dataset.nodata  # NoData-Wert auslesen
    print("Skalierungsfaktor:", dataset.scales) 

# NoData-Werte mit NaN ersetzen
band1 = np.where(band1 == nodata, np.nan, band1)
 # Sollte [1] sein, falls keine Skalierung nötig

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

quit()#













