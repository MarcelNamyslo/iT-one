import folium
import geopandas as gpd
import pandas as pd
import numpy as np
from folium.plugins import HeatMap
from folium.features import GeoJsonTooltip, GeoJsonPopup

# 📌 1. Admin Layer (Shapefile) mit Distrikten laden
admin_gdf = gpd.read_file(r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Admin_layers\Assaba_Districts_layer.shp")

# 📌 2. Straßen & Flüsse laden
road_loc = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Streamwater_Line_Road_Network\Main_Road.shp"
water_loc = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Streamwater_Line_Road_Network\Streamwater.shp"
roads_gdf = gpd.read_file(road_loc)
waters_gdf = gpd.read_file(water_loc)

# 📌 3. Niederschlags- & Vegetationspunkte laden
all_points_df = pd.read_csv("updated_merged_data.csv")  # ✅ Deine CSV mit 1.200 Datenpunkten pro Jahr

# Falls CSV keine Geometrie hat → in GeoDataFrame umwandeln
all_points_gdf = gpd.GeoDataFrame(all_points_df, geometry=gpd.points_from_xy(all_points_df.Longitude, all_points_df.Latitude), crs="EPSG:4326")


# 📌 4. Mittelpunkt für die Karte berechnen
center_lat = admin_gdf.geometry.centroid.y.mean()
center_lon = admin_gdf.geometry.centroid.x.mean()

# 📌 5. Folium-Karte erstellen
m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles="cartodb positron")

# 📌 6. Heatmap-Daten vorbereiten (Punkte + Wert für Farbintensität)
heat_data = list(zip(all_points_gdf["Longitude"], all_points_gdf["Latitude"], all_points_gdf["Classification"]))


# 📌 7. Fließende Heatmap hinzufügen
HeatMap(
    heat_data,
    radius=20,  # Erhöht den Radius für einen weicheren Übergang
    blur=15,    # Erhöht die Weichheit der Heatmap
    max_zoom=12,
    gradient={
        str(0.2): "blue",   # Wenig Werte → Blau
        str(0.6): "cyan",   # Leicht mehr → Cyan
        str(0.8): "lime",   # Mittel → Grün
        str(0.95): "yellow", # Höhere Werte → Gelb
        str(1.0): "red"     # Höchste Werte → Rot
    }
).add_to(m)

# 📌 8. Bezirksgrenzen mit Hover-Mean-Werten anzeigen
mean_values = all_points_gdf.groupby("FID_1")[["Absorption", "Precipitation", "Classification"]].mean().reset_index()
admin_gdf = admin_gdf.merge(mean_values, on="FID_1", how="left")

date_columns = ["date", "validOn", "validTo"]
for col in date_columns:
    if col in admin_gdf.columns:
        admin_gdf[col] = admin_gdf[col].astype(str)  # Konvertiere Datum zu String

folium.GeoJson(
    admin_gdf,
    name="Districts (Mean Values)",
    style_function=lambda feature: {
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.3,
        "fillColor": "gray"
    },
    highlight_function=lambda feature: {
        "fillColor": "red",
        "fillOpacity": 0.7,
        "color": "black",
        "weight": 3
    },
    tooltip=GeoJsonTooltip(fields=["ADM3_EN"],
                           aliases=["District:"]),
    popup=GeoJsonPopup(fields=["ADM3_EN", "Precipitation", "Absorption", "Classification"],
                       aliases=["City:", "Mean Precipitation:", "Mean Absorption:", "Mean Classification:"])
).add_to(m)

# 📌 9. Straßen hinzufügen (Grau)
folium.GeoJson(
    roads_gdf,
    name="Roads",
    style_function=lambda feature: {
        "color": "gray",
        "weight": 1.5,
        "opacity": 0.8
    }
).add_to(m)

# 📌 10. Flüsse hinzufügen (Blau)
folium.GeoJson(
    waters_gdf,
    name="Rivers",
    style_function=lambda feature: {
        "color": "blue",
        "weight": 1.5,
        "opacity": 0.8
    }
).add_to(m)

# 📌 11. Labels mit den Städtenamen setzen
for _, row in admin_gdf.iterrows():
    centroid = row.geometry.centroid
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(html=f"<div style='font-size:10px; color:black;'>{row['ADM3_EN']}</div>")
    ).add_to(m)

# 📌 12. Layer Control zum Umschalten der Ebenen hinzufügen
folium.LayerControl().add_to(m)

# 📌 13. Karte speichern
m.save("districts_heatmap_2024.html")
print("✅ Karte gespeichert: districts_heatmap.html")
