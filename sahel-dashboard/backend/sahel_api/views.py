import os
import rasterio
import numpy as np
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from io import BytesIO
from rasterio.mask import mask
from shapely.geometry import mapping
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from shapely.ops import unary_union
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
    data_path1 = settings.HTML_ROOT
    files = []
    files1 = []

    if not os.path.exists(data_path):
        return JsonResponse({"error": "Data folder not found"}, status=404)

    # Traverse MEDIA_ROOT and include folder structure
    for root, _, filenames in os.walk(data_path):
        for filename in filenames:
            if filename.endswith(".tif"):
                # Get relative path including subfolders
                relative_path = os.path.relpath(os.path.join(root, filename), data_path)
                files.append(relative_path.replace("\\", "/"))  # Normalize for Windows
            
    for root, _, filenames in os.walk(data_path1):
        for filename in filenames:        
            if filename.endswith(".html"):
                relative_path = os.path.relpath(os.path.join(root, filename), data_path)
                files1.append(relative_path.replace("\\", "/"))

    return JsonResponse({
        "files": files,
        "files1": files1  # ✅ Now returned
    })

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
        # Folder paths
        precipitation_tif_folder = r"C:\iT-one\sahel-dashboard\backend\data\Datasets_Hackathon\Climate_Precipitation_Data"
        gpp_tif_folder = r"C:\iT-one\sahel-dashboard\backend\data\Datasets_Hackathon\MODIS_Gross_Primary_Production_GPP"
        shapefile_path = r"C:\iT-one\sahel-dashboard\backend\data\Datasets_Hackathon\Admin_layers\Assaba_Districts_layer.shp"

        try:
            # Read region shapefile
            regions_gdf = gpd.read_file(shapefile_path)

            data = json.loads(request.body)
            district_name = data.get("city", "").strip()
            print("Requested District:", district_name)

            target_region = regions_gdf[regions_gdf["ADM3_EN"] == district_name]
            print("Target Region:", target_region)

            if target_region.empty:
                return JsonResponse({"error": f"Region '{district_name}' not found."}, status=404)

            # ✅ Define the geometry once after checking target_region is not empty
            from shapely.ops import unary_union
            target_geometry = target_region.geometry.unary_union

            # Initialize results
            precipitation_stats = {}
            gpp_stats = {}

            print(1)

            # =========================
            # 1. Process Precipitation
            # =========================
            for filename in os.listdir(precipitation_tif_folder):
                if filename.lower().endswith(".tif"):
                    m = re.search(r'(\d{4})', filename)
                    if not m:
                        continue
                    year = m.group(1)

                    file_path = os.path.join(precipitation_tif_folder, filename)
                    with rasterio.open(file_path) as dataset:
                        # Clip raster to region polygon
                        clipped_image, _ = mask(dataset, [mapping(target_region.geometry.iloc[0])], crop=True)
                        band = clipped_image[0]
                        nodata = dataset.nodata

                        valid_mask = band != nodata
                        if not np.any(valid_mask):
                            continue

                        mean_value = band[valid_mask].mean()
                        precipitation_stats[year] = mean_value

            # ====================
            # 2. Process GPP Data
            # ====================
            gpp_data = []

            print(2)
            try:
                for filename in os.listdir(gpp_tif_folder):
                    if filename.lower().endswith(".tif"):
                        m = re.search(r'(\d{4})', filename)
                        if not m:
                            continue
                        year = m.group(1)

                        file_path = os.path.join(gpp_tif_folder, filename)
                        with rasterio.open(file_path) as dataset:
                            try:
                                # Reproject the region polygon to match raster CRS
                                geometry_for_mask = gpd.GeoSeries([target_geometry], crs=target_region.crs).to_crs(dataset.crs).iloc[0]

                                # Clip raster to the region
                                clipped_image, _ = mask(dataset, [mapping(geometry_for_mask)], crop=True)
                                band = clipped_image[0]
                                nodata = dataset.nodata

                                valid_mask = band != nodata
                                if not np.any(valid_mask):
                                    continue

                                mean_value = band[valid_mask].mean()
                                gpp_stats[year] = mean_value

                            except Exception as e:
                                print(f"Error processing {filename}: {e}")


            except Exception as e:
                print({"error": str(e)})
                return JsonResponse({"error": str(e)}, status=500)
            # Final combined return
            print("???????????????")

            precipitation_stats = {year: float(val) for year, val in precipitation_stats.items()}
            gpp_stats = {year: float(val) for year, val in gpp_stats.items()}

            response_data = {
                "message": "Data computed successfully",
                "stats": precipitation_stats,
                "gpp": gpp_stats
            }
            print("response_data: " + str(response_data))
            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
