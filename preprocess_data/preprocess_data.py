import rasterio
import pandas as pd
import geopandas as gpd
import rasterio.warp
import numpy as np
from scipy.interpolate import griddata
from shapely.geometry import Point
import matplotlib.pyplot as plt
import folium

year_values = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023]

# Sinusoidal CRS für MODIS-Daten (Temperature und Population)
sinusoidal_crs = rasterio.crs.CRS.from_proj4('+proj=sinu +R=6371007.181 +nadgrids=@null +wktext')

# Automatische Reprojektion von Sinusoidal nach WGS84 (EPSG:4326)
def reproject_to_wgs84(raster_path):
    with rasterio.open(raster_path) as src:
        # Falls das Raster schon in EPSG:4326 ist, keine Umwandlung nötig
        if src.crs == "EPSG:4326":
            print(f"✅ {raster_path} ist bereits in EPSG:4326.")
            return raster_path
        
        print(f"🔄 {raster_path} wird nach EPSG:4326 transformiert...")

        # Berechne Transformation
        transform, width, height = rasterio.warp.calculate_default_transform(
            src.crs, "EPSG:4326", src.width, src.height, *src.bounds
        )

        # Erstelle neue Metadaten für das umprojizierte Raster
        kwargs = src.meta.copy()
        kwargs.update({
            "crs": "EPSG:4326",
            "transform": transform,
            "width": width,
            "height": height
        })

        # Speichere das umgewandelte Raster mit einem neuen Namen
        reprojected_path = raster_path.replace(".tif", "_reprojected.tif")
        with rasterio.open(reprojected_path, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                rasterio.warp.reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs="EPSG:4326",
                    resampling=rasterio.enums.Resampling.nearest
                )

        print(f"✅ Umwandlung abgeschlossen: {reprojected_path}")
        return reprojected_path

from scipy.spatial import cKDTree

def downsample_to_low_res(high_res_gdf, low_res_gdf, value_column):
    """
    Aggregiert hochauflösende Daten (Temperature, Population) auf die niedrige Auflösung von Rainfall GDF.
    """
    # Koordinaten für schnelles Matching
    high_res_coords = np.array(list(zip(high_res_gdf.Longitude, high_res_gdf.Latitude)))
    low_res_coords = np.array(list(zip(low_res_gdf.Longitude, low_res_gdf.Latitude)))

    # KdTree für schnellstes Nearest-Neighbor Mapping
    tree = cKDTree(low_res_coords)
    _, idxs = tree.query(high_res_coords)  # Finde die nächste niedrige Rasterzelle für jeden Hochauflösungs-Punkt

    # Weise jedem hochauflösenden Punkt seine zugeordnete niedrige Rasterzelle zu
    high_res_gdf["nearest_low_res_idx"] = idxs

    # Aggregierte Werte für jede Niederschlags-Zelle berechnen
    aggregated_values = high_res_gdf.groupby("nearest_low_res_idx")[value_column].mean()

    # Jetzt sicherstellen, dass wir NUR für existierende `low_res_gdf`-Punkte schreiben!
    low_res_gdf[value_column] = low_res_gdf.index.map(aggregated_values).fillna(0)

    return low_res_gdf

# Funktion zum Konvertieren von Raster zu Punkten
def raster_to_points(raster_path, var_name):
    with rasterio.open(raster_path) as dataset:
        band1 = dataset.read(1)
        transform = dataset.transform
        height, width = band1.shape

        points = []
        for row in range(height):
            for col in range(width):
                lon, lat = dataset.xy(row, col)
                value = band1[row, col]
                if value != dataset.nodata:
                    points.append((lon, lat, value))

        df = pd.DataFrame(points, columns=["Longitude", "Latitude", var_name])
        return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326")
    
for i in year_values:
    climate_data = fr"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Climate_Precipitation_Data\{i}R.tif"
    gpp_data = fr"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\MODIS_Gross_Primary_Production_GPP\{i}_GP.tif"
    land_data = fr"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Modis_Land_Cover_Data\{i}LCT.tif"
    admin_layer_loc = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Admin_layers\Assaba_Districts_layer.shp"
    road_loc = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Streamwater_Line_Road_Network\Main_Road.shp"
    water_loc = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Streamwater_Line_Road_Network\Streamwater.shp"
    round_down_year = i - (i % 5)
    pop_density = fr"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Gridded_Population_Density_Data\Assaba_Pop_{round_down_year}.tif"

    gpp_data = reproject_to_wgs84(gpp_data)
    land_data = reproject_to_wgs84(land_data)

    rainfall_gdf = raster_to_points(climate_data, "Precipitation")
    vegetation_gdf = raster_to_points(gpp_data, "Absorption")
    population_gdf = raster_to_points(pop_density, "Population")
    classification_gdf = raster_to_points(land_data, "Classification")
    vegetation_gdf = vegetation_gdf[vegetation_gdf["Absorption"] != 65533]
    i # Interpolation: Rainfall auf Temperature GDF skalieren
    # Temperatur runter skalieren auf Niederschlagsraster
    rainfall_gdf = downsample_to_low_res(vegetation_gdf, rainfall_gdf, "Absorption")

    # Population runter skalieren
    rainfall_gdf = downsample_to_low_res(population_gdf, rainfall_gdf, "Population")

    # Vegetation runter skalieren
    rainfall_gdf = downsample_to_low_res(classification_gdf, rainfall_gdf, "Classification")
        #elevation_gdf = raster_to_points(road_loc, "Elevation")
    # Shapefile mit administrativen Regionen laden
    regions_gdf = gpd.read_file(admin_layer_loc)

    # Spatial Join: Punkte mit den Regionen verknüpfen
    joined_gdf = gpd.sjoin(rainfall_gdf, regions_gdf, how="inner", predicate="within")

    # Ergebnisse speichern & ausgeben
    print(joined_gdf.head())

    # Speichern als CSV oder GeoJSON falls benötigt
    joined_gdf.to_csv(f"joined_data_{i}.csv", index=False)
    joined_gdf.to_file(f"joined_data_{i}.geojson", driver="GeoJSON")

    print(f"✅ Daten für {i} gespeichert!\n")
    continue

    """    
    # Mittelpunkt der Karte berechnen
    center_lat = joined_gdf.geometry.centroid.y.mean()
    center_lon = joined_gdf.geometry.centroid.x.mean()

    # Karte erstellen
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    def style_function(row):
        density = row.get("Population Density", 0)  # Direkter Zugriff auf `joined_gdf`
        return {
            "fillColor": "green" if density > 100 else "yellow",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.6
        }


    # Regionen mit allen Daten als Tooltip
    for _, row in joined_gdf.iterrows():
        tooltip_text = """f"""
            <b>Region:</b> {row.get('Region_ID', 'Unbekannt')}<br>
            🌧️ <b>Precipitation:</b> {row.get('Precipitation', 'N/A')} mm<br>
            🌡️ <b>Absorption:</b> {row.get('Absorption', 'N/A')}<br>
            👨‍👩‍👧‍👦 <b>Population Density:</b> {row.get('Population Density', 'N/A')} Einw/km²<br>
            🌿 <b>Vegetation Index:</b> {row.get('Vegetation Index', 'N/A')}
        """
    """
        folium.GeoJson(
            row.geometry,
            name=row.get("Region_ID", "Unbekannt"),
            tooltip=folium.Tooltip(tooltip_text, sticky=True),
            style_function=style_function
        ).add_to(m)

    # Karte speichern
    m.save("full_region_map.html")
    print("✅ Interaktive Karte gespeichert: full_region_map.html")

    quit()
    """
















    temperature_gdf = temperature_gdf.drop(columns=["geometry"])
    population_gdf = population_gdf.drop(columns=["geometry"])
    vegetation_gdf = vegetation_gdf.drop(columns=["geometry"])
    # Prüfe, ob die einzigartigen Koordinaten in jedem DataFrame wirklich übereinstimmen
    print("Anzahl einzigartiger Koordinaten:")
    print("Rainfall:", rainfall_gdf[["Longitude", "Latitude"]].drop_duplicates().shape)
    print("Temperature:", temperature_gdf[["Longitude", "Latitude"]].drop_duplicates().shape)
    print("Population:", population_gdf[["Longitude", "Latitude"]].drop_duplicates().shape)
    print("Vegetation:", vegetation_gdf[["Longitude", "Latitude"]].drop_duplicates().shape)


    # Alle Punkt-Daten kombinieren
    merged_points = rainfall_gdf.merge(temperature_gdf, on=["Longitude", "Latitude"]) \
                                .merge(population_gdf, on=["Longitude", "Latitude"]) \
                                .merge(vegetation_gdf, on=["Longitude", "Latitude"])

    # In GeoDataFrame konvertieren
    merged_gdf = gpd.GeoDataFrame(merged_points, geometry=gpd.points_from_xy(merged_points.Longitude, merged_points.Latitude), crs="EPSG:4326")
    # Prüfe, ob die Werte exakt gleich sind
    merged_test = rainfall_gdf.merge(temperature_gdf, on=["Longitude", "Latitude"], how="inner")
    print(f"Nach dem ersten Merge: {merged_test.shape}")

    regions_gdf = gpd.read_file(admin_layer_loc)
    print("CRS von merged_gdf:", merged_gdf.crs)
    print("CRS von regions_gdf:", regions_gdf.crs)
    # Spatial Join: Punkte mit den Regionen verknüpfen
    joined_gdf = gpd.sjoin(merged_gdf, regions_gdf, how="inner", predicate="within")

    print(joined_gdf.head())
    # Open a file for writing (will create it if it doesn't exist)
    with open("output.txt", "w") as file:
        file.write(str(merged_gdf))

    print("Text has been written to output.txt")
    quit()
