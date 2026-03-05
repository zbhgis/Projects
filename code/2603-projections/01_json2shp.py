"""
-------------------------------------------------------------------------------
@Author         :  zbhgis
@Github         :  https://github.com/zbhgis
@Description    :  convert json to shapefile
-------------------------------------------------------------------------------
"""

import json
import random
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


def json2shp(
    json_path,
    output_shp_path,
    keep_count=100,
    lon_field="Longitude",
    lat_field="Latitude",
    crs="EPSG:4326",
):
    # 打开数据
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 数据抽样
    sampled_data = random.sample(data, keep_count)
    df = pd.DataFrame(sampled_data)
    df = df[[lon_field, lat_field]]

    # 字段重命名
    df = df.rename(columns={lon_field: "lon", lat_field: "lat"})
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")

    # 颜色字段
    df["level"] = [random.randint(1, 5) for _ in range(len(df))]

    # 生成gdf
    geometry = [Point(xy) for xy in zip(df["lon"], df["lat"])]
    gdf = gpd.GeoDataFrame(
        df.drop(columns=["lon", "lat"]),
        geometry=geometry,
        crs=crs,
    )

    gdf.to_file(output_shp_path, encoding="utf-8")


if __name__ == "__main__":
    json_file = "./data_origin/data.json"
    shp_file = "./data_res/points_land.shp"

    json2shp(
        json_path=json_file,
        output_shp_path=shp_file,
        keep_count=100,
        lon_field="Longitude",
        lat_field="Latitude",
        crs="EPSG:4326",
    )

    json_file = "./data_origin/resource.json"
    shp_file = "./data_res/points_ocean.shp"

    json2shp(
        json_path=json_file,
        output_shp_path=shp_file,
        keep_count=100,
        lon_field="Long",
        lat_field="Lat",
        crs="EPSG:4326",
    )

    print("OK")
