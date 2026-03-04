import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import rasterio
import geopandas as gpd
from matplotlib.lines import Line2D
import numpy as np

plt.rcParams["font.family"] = "Arial"
boundary_shp = "./data_res/boundary.shp"
points_land_shp = "./data_res/points_land.shp"
points_ocean_shp = "./data_res/points_ocean.shp"
dem_tif = "./data_res/gebco_dem.tif"

fig = plt.figure(figsize=(14, 10), dpi=100)
projections = [
    ("Mercator", ccrs.Mercator()),
    ("Robinson", ccrs.Robinson()),
    ("EqualEarth", ccrs.EqualEarth()),
    ("GoodeHomolosine", ccrs.InterruptedGoodeHomolosine()),
    ("SpilhausAdams", ccrs.Spilhaus()),
    ("OrthographicNorth", ccrs.Orthographic(central_longitude=0, central_latitude=90)),
    ("OrthographicEquator", ccrs.Orthographic(central_longitude=0, central_latitude=0)),
    ("OrthographicSouth", ccrs.Orthographic(central_longitude=0, central_latitude=-90)),
]
proj_name, proj_obj = projections[1]
ax = fig.add_subplot(1, 1, 1, projection=proj_obj)

ax.set_global()
# 添加DEM数据
with rasterio.open(dem_tif) as src:
    dem_data = src.read(1, masked=True)
    left, bottom, right, top = src.bounds
    extent = [left, right, bottom, top]

    im = ax.imshow(
        dem_data,
        extent=extent,
        transform=ccrs.PlateCarree(),
        origin="upper",
        cmap="gist_earth",
        vmin=-6000,
        vmax=6000,
        alpha=0.8,
        interpolation="bilinear",
    )

# 添加DEM色带
cbar = fig.colorbar(
    im,
    ax=ax,
    orientation="horizontal",
    pad=0.04,
    aspect=40,
    shrink=0.6,
)
cbar.ax.tick_params(
    labelsize=16,
    labelcolor="black",
    length=4,
)
cbar.set_label("Elevation(m)", fontsize=18)

# 添加矢量边界数据
reader = shpreader.Reader(boundary_shp)
boundary_feature = cfeature.ShapelyFeature(
    reader.geometries(),
    ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="#928F8F",
    linewidth=2.0,
    linestyle="-",
)
ax.add_feature(boundary_feature, zorder=10)

# 添加陆地点数据
gdf = gpd.read_file(points_land_shp)
lons = gdf.geometry.x
lats = gdf.geometry.y

# 生成陆地点数据颜色
color_map_land = {
    1: "#E6F3FF",
    2: "#B3D9FF",
    3: "#80BFFF",
    4: "#4DA6FF",
    5: "#0066CC",
}
colors = [color_map_land.get(level, "gray") for level in gdf["level"]]

# 绘制陆地点数据
ax.scatter(
    lons,
    lats,
    s=100,
    c=colors,
    edgecolor="black",
    linewidth=0.8,
    alpha=0.9,
    transform=ccrs.PlateCarree(),
    zorder=10,
)

# 添加陆地点图例
legend_elements_land = [
    Line2D(
        [0],
        [0],
        marker="o",
        linestyle="none",
        label=f"Level {l}",
        markerfacecolor=color,
        markersize=10,
        markeredgecolor="black",
    )
    for l, color in color_map_land.items()
]
legend_land = ax.legend(
    handles=legend_elements_land,
    loc="lower left",
    title="Level",
    title_fontsize=18,
    fontsize=16,
    frameon=True,
    edgecolor="black",
    facecolor="white",
    framealpha=0.95,
)
legend_land.set_zorder(15)
ax.add_artist(legend_land)

# 相同方法再添加一次海洋点数据
gdf = gpd.read_file(points_ocean_shp)
lons = gdf.geometry.x
lats = gdf.geometry.y

# 生成海洋点数据尺寸
size_map_ocean = {
    1: 50,
    2: 100,
    3: 150,
    4: 200,
    5: 250,
}
sizes = [size_map_ocean.get(level, 0) for level in gdf["level"]]

# 绘制海洋点数据
ax.scatter(
    lons,
    lats,
    s=sizes,
    c="#9F9C9C",
    edgecolor="black",
    linewidth=0.8,
    alpha=0.9,
    transform=ccrs.PlateCarree(),
    zorder=10,
)

# 添加海洋点图例
legend_elements_ocean = [
    Line2D(
        [0],
        [0],
        marker="o",
        linestyle="none",
        label=f"Level {s}",
        markerfacecolor="#9F9C9C",
        markersize=np.sqrt(size),
        markeredgecolor="black",
    )
    for s, size in size_map_ocean.items()
]
legend_ocean = ax.legend(
    handles=legend_elements_ocean,
    loc="lower right",
    title="Level",
    title_fontsize=18,
    fontsize=16,
    frameon=True,
    edgecolor="black",
    facecolor="white",
    framealpha=0.95,
)
legend_ocean.set_zorder(15)

# 添加经纬度标签
gl = ax.gridlines(
    draw_labels=False,
    linewidth=0.5,
    color="gray",
    alpha=0.4,
    linestyle="--",
)

# 添加图名
ax.set_title(proj_name, fontsize=20, pad=10)

plt.tight_layout()
plt.savefig(
    f"./fig_res/gebco_dem_{proj_name}.png",
    dpi=100,
    bbox_inches="tight",
    facecolor="white",
)
print("ok")
