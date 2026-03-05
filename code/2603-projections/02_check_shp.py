"""
-------------------------------------------------------------------------------
@Author         :  zbhgis
@Github         :  https://github.com/zbhgis
@Description    :  check and copy shapefile
-------------------------------------------------------------------------------
"""

import geopandas as gpd
import os
import shutil


def check_file(shp_path):
    gdf = gpd.read_file(shp_path)
    if gdf.crs is None:
        print("未定义坐标系")
    elif gdf.crs.to_epsg() == 4326:
        print("EPSG:4326")
    elif gdf.crs.to_epsg() is not None:
        print(f"EPSG:{gdf.crs.to_epsg()}")


def copy_shapefile(shp_path, output_folder, new_base_name):
    base_dir = os.path.dirname(shp_path)
    base_name = os.path.splitext(os.path.basename(shp_path))[0]
    extensions = [".shp", ".shx", ".dbf", ".prj", ".cpg", ".sbn", ".sbx", ".shp.xml"]

    copied = 0
    for ext in extensions:
        src_file = os.path.join(base_dir, base_name + ext)
        if os.path.exists(src_file):
            dst_file = os.path.join(output_folder, new_base_name + ext)
            shutil.copy2(src_file, dst_file)
            copied += 1

    if copied > 0:
        print(f"成功复制")
    else:
        print("复制失败")


if __name__ == "__main__":
    shp = "./data_origin/continent.shp"
    target_folder = "./data_res"
    check_file(shp)
    copy_shapefile(shp, target_folder, "boundary")
