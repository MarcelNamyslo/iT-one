import folium
import geopandas as gpd
import pandas as pd
import numpy as np
from folium.plugins import HeatMap
from folium.features import GeoJsonTooltip, GeoJsonPopup
import os

# 📌 1. Admin Layer (Shapefile) mit Distrikten laden

# 📌 2. Straßen & Flüsse laden
road_loc = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Streamwater_Line_Road_Network\Main_Road.shp"
water_loc = r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Streamwater_Line_Road_Network\Streamwater.shp"
roads_gdf = gpd.read_file(road_loc)
waters_gdf = gpd.read_file(water_loc)

# 📌 3. Funktion zur Erstellung der Heatmaps pro Jahr und Distrikt
def create_heatmap_for_district(year, district_id):
    admin_gdf = gpd.read_file(r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Admin_layers\Assaba_Districts_layer.shp")
    # Lade die entsprechende CSV mit den Datenpunkten für das Jahr
    all_points_df = pd.read_csv(f"joined_data_{year}.csv")
    
    # Filtere Daten für den spezifischen Distrikt
    district_data = all_points_df[all_points_df["FID_1"] == district_id]
    
    # Falls CSV keine Geometrie hat → in GeoDataFrame umwandeln
    district_gdf = gpd.GeoDataFrame(district_data, geometry=gpd.points_from_xy(district_data.Longitude, district_data.Latitude), crs="EPSG:4326")
    
    # 📌 4. Mittelpunkt für die Karte berechnen
    center_lat = district_gdf.geometry.centroid.y.mean()
    center_lon = district_gdf.geometry.centroid.x.mean()
    
    # 📌 5. Folium-Karte für den Distrikt erstellen
    m = folium.Map(location=[center_lat, center_lon], zoom_start=9, tiles="cartodb positron")

    # 📌 6. Heatmap-Daten vorbereiten (Punkte + Wert für Farbintensität)
    heat_data = list(zip(district_gdf.Latitude, district_gdf.Longitude, district_gdf["Precipitation"]))
    
    # 📌 7. Heatmap hinzufügen
    HeatMap(
        heat_data,
        radius=20,
        blur=15,
        max_zoom=12,
        gradient={
            str(0.2): "yellow",  
            str(0.85): "lime",   
            str(0.9): "green",   
            str(0.95): "blue",  
            str(1.0): "purple"   
        }
    ).add_to(m)
    
    # 📌 8. Bezirksgrenzen mit Hover-Mean-Werten anzeigen
    mean_values = district_gdf.groupby("FID_1")[["Absorption", "Precipitation", "Classification"]].mean().reset_index()
    admin_gdf = admin_gdf.merge(mean_values, on="FID_1", how="left")

    date_columns = ["date", "validOn", "validTo"]
    for col in date_columns:
        if col in admin_gdf.columns:
            admin_gdf[col] = admin_gdf[col].astype(str)  # Konvertiere Datum zu String

    folium.GeoJson(
        admin_gdf[admin_gdf["FID_1"] == district_id],  # Nur den aktuellen Distrikt einblenden
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
        tooltip=GeoJsonTooltip(fields=["ADM3_EN", "Precipitation"],
                               aliases=["District:", "Mean Precipitation:"]),
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

    # 📌 11. Label mit dem Namen des Distrikts hinzufügen
    for _, row in admin_gdf[admin_gdf["FID_1"] == district_id].iterrows():
        centroid = row.geometry.centroid
        folium.Marker(
            location=[centroid.y, centroid.x],
            icon=folium.DivIcon(html=f"<div style='font-size:12px; color:black;'>{row['ADM3_EN']}</div>")
        ).add_to(m)

    # 📌 11. Karte speichern
    # Erstelle Verzeichnisse für jedes Jahr und Distrikt
    directory = f"maps/{year}/{district_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Speichern der Karte für den Distrikt
    m.save(f"{directory}/district_heatmap_{district_id}.html")
    print(f"✅ Karte für Distrikt {district_id}, Jahr {year} gespeichert!")
    
admin_gdf = gpd.read_file(r"C:\Users\paulb\PycharmProjects\start_hack_25_data\Datasets_Hackathon 1\Datasets_Hackathon\Admin_layers\Assaba_Districts_layer.shp")

# 📌 12. Für jedes Jahr und jeden Distrikt eine Karte erstellen
years = range(2010, 2024)
for year in years:
    # Für jedes Jahr alle Distrikte durchlaufen
    for district_id in admin_gdf["FID_1"]:
        create_heatmap_for_district(year, district_id)
