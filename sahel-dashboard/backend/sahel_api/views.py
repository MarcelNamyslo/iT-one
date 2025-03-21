import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import geopandas as gpd
import pandas as pd
import re
import json
@api_view(['GET'])
def list_files(request):
    """
    Returns a list of available TIFF files from MEDIA_ROOT, including folder structure.
    """
    data_path = settings.MEDIA_ROOT  # Directory where TIFF files are stored
    files = []

    if not os.path.exists(data_path):
        return JsonResponse({"error": "Data folder not found"}, status=404)

    # Traverse MEDIA_ROOT and include folder structure
    for root, _, filenames in os.walk(data_path):
        for filename in filenames:
            if filename.endswith(".tif"):
                # Get relative path including subfolders
                relative_path = os.path.relpath(os.path.join(root, filename), data_path)
                files.append(relative_path.replace("\\", "/"))  # Normalize for Windows

    return JsonResponse({"files": files})

@api_view(['GET'])
def list_html_maps(request):
    """
    Returns a list of available HTML maps in the `html_maps` folder.
    """
    maps_dir = os.path.join(settings.MEDIA_ROOT, "html_maps")
    if not os.path.exists(maps_dir):
        return JsonResponse({"error": "HTML maps folder not found"}, status=404)

    files = [f for f in os.listdir(maps_dir) if f.endswith(".html")]
    return JsonResponse({"html_maps": files})

@api_view(['GET'])
def process_tiff(request, filepath):
    """
    Processes a TIFF file and returns a PNG image.
    """
    TIFF_DIRECTORY = settings.MEDIA_ROOT  # Root directory where TIFFs are stored
    tiff_path = os.path.join(TIFF_DIRECTORY, filepath)  # Use dynamic path

    print(f"🔍 Trying to load file: {tiff_path}")  # Debugging output

    if not os.path.exists(tiff_path):
        print(f"❌ File not found: {tiff_path}")
        return JsonResponse({"error": "File not found", "path": tiff_path}, status=404)

    try:
        # Open the TIFF file
        with rasterio.open(tiff_path) as dataset:
            band1 = dataset.read(1)  # Read the first band
            nodata = dataset.nodata  # Get NoData value

        # Replace NoData values with NaN
        band1 = np.where(band1 == nodata, np.nan, band1)

        # Create a plot
        fig, ax = plt.subplots(figsize=(6, 8))
        cax = ax.imshow(band1, cmap="viridis", interpolation="nearest")
        fig.colorbar(cax, label="Pixel values")
        ax.set_title(f"Raster Data: {filepath}")

        # Save plot to a BytesIO stream
        image_stream = BytesIO()
        plt.savefig(image_stream, format="png", bbox_inches="tight")
        plt.close(fig)

        # Return PNG response
        image_stream.seek(0)
        return HttpResponse(image_stream.getvalue(), content_type="image/png")

    except Exception as e:
        return JsonResponse({"error": f"Failed to process TIFF: {str(e)}"}, status=500)


@csrf_exempt  # 🚨 TEMPORARILY disable CSRF protection for debugging
def save_map_data(request):
    """
    Loops through all TIFF files (one per year) and computes the mean precipitation 
    for the region with FID_1 == 66, returning a JSON mapping year -> mean precipitation.
    """
    if request.method == "POST":
        # Folder containing the TIFF files
        tif_folder = r"C:\iT-one\sahel-dashboard\backend\data\Datasets_Hackathon\Climate_Precipitation_Data"
        # Path to the shapefile with administrative boundaries
        shapefile_path = r"C:\iT-one\sahel-dashboard\backend\data\Datasets_Hackathon\Admin_layers\Assaba_Districts_layer.shp"
        
        try:
            # Read the region shapefile using GeoPandas
            regions_gdf = gpd.read_file(shapefile_path)
            # Filter for the target region with FID_1 equal to 66

            data = json.loads(request.body)
            district_name = data.get("city", "").strip()
            print(district_name)

            target_region = regions_gdf[regions_gdf["ADM3_EN"] == district_name]
            
            if target_region.empty:
                return JsonResponse({"error": "Region with FID_1 66 not found."}, status=404)

            # Dictionary to hold the statistics per year
            stats = {}

            # Loop over all TIFF files in the folder
            for filename in os.listdir(tif_folder):
                if filename.lower().endswith(".tif"):
                    file_path = os.path.join(tif_folder, filename)
                 
                    # Extract year from the filename (assuming a four-digit year appears in the name)
                    m = re.search(r'(\d{4})', filename)
                    if not m:
                        continue  # Skip files without a year in the name
                    year = m.group(1)

                    # Open the TIFF file
                    with rasterio.open(file_path) as dataset:
                        band1 = dataset.read(1)
                        nodata = dataset.nodata
                        rows, cols = band1.shape
                    
                        # Collect all valid (lon, lat, value) tuples
                        data = []
                        for row in range(rows):
                            for col in range(cols):
                                value = band1[row, col]
                                if value == nodata:
                                    continue
                                lon, lat = dataset.xy(row, col)
                                data.append((lon, lat, value))
                        
                        # Skip if no valid data found
                        if not data:
                            continue
                        
                        # Create a DataFrame from the raster data
                        df = pd.DataFrame(data, columns=["Longitude", "Latitude", "Precipitation"])
                        # Convert DataFrame to a GeoDataFrame
                        raster_gdf = gpd.GeoDataFrame(
                            df, 
                            geometry=gpd.points_from_xy(df.Longitude, df.Latitude),
                            crs=dataset.crs
                        )
                        
                        # Ensure both GeoDataFrames share the same CRS (transform if necessary)
                        if raster_gdf.crs != target_region.crs:
                            raster_gdf = raster_gdf.to_crs(target_region.crs)
                        
                        # Perform a spatial join to find points within the target region
                        joined = gpd.sjoin(raster_gdf, target_region, how="inner", predicate="within")
                        
                        if joined.empty:
                            # No data points fall within the target region for this file
                            continue
                        
                        # Compute the mean precipitation for the region
                        mean_precip = joined["Precipitation"].mean()
                        stats[year] = mean_precip
                        

            # Return the computed statistics as JSON
            stats = {year: float(value) for year, value in stats.items()}
            print(stats)
            return JsonResponse({"message": "Data computed successfully", "stats": stats}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)