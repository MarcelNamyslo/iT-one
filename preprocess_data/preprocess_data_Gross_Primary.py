import rasterio
import numpy as np
import matplotlib.pyplot as plt

tif_file = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\MODIS_Gross_Primary_Production_GPP\2023_GP.tif"

with rasterio.open(tif_file) as dataset:
    print(dataset.count)
    band1 = dataset.read(1)  # Erstes Band
    nodata = dataset.nodata  # NoData-Wert auslesen
    print(dataset.transform)
    print("hier")
    print(dataset.crs)
    print("hier")
    print("Skalierungsfaktor:", dataset.scales) 

    # Ungültige Werte (65533.0) durch NaN ersetzen
    band1 = np.where(band1 == 65533.0, np.nan, band1)

    # NoData-Werte mit NaN ersetzen
    band1 = np.where(band1 == nodata, np.nan, band1)

    # Min & Max Werte im Raster prüfen
    print(np.unique(band1))  # Gibt dir eine Liste aller Werte
    print("Min. Wert:", np.nanmin(band1))
    print("Max. Wert:", np.nanmax(band1))

    # Histogramm der Rasterwerte anzeigen
    plt.hist(band1[~np.isnan(band1)].flatten(), bins=50, color="blue", alpha=0.7)
    plt.xlabel("Pixelwerte")
    plt.ylabel("Anzahl der Pixel")
    plt.title("Histogramm der Rasterwerte")
    plt.show()

    # Raster mit NoData-Maske plotten
    plt.figure(figsize=(6, 8))
    plt.imshow(band1, cmap="viridis", interpolation="nearest")
    plt.colorbar(label="Pixelwerte")
    plt.title("Rasterdaten ohne ungültige Werte (65533.0)")
    plt.show()

quit()
