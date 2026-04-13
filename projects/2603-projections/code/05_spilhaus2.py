"""
-------------------------------------------------------------------------------
@Author         :  zbhgis
@Github         :  https://github.com/zbhgis
@Description    :  spilhaus with gradient blue basemap
-------------------------------------------------------------------------------
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import rasterio
import matplotlib.colors as mcolors


plt.rcParams["font.family"] = "Arial"
dem_tif = "../data_res/gebco_dem.tif"
fig = plt.figure(figsize=(10, 10), dpi=100)
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Spilhaus())
ax.set_global()
ax.add_feature(cfeature.LAND, facecolor="white", edgecolor="none", zorder=1)
ax.coastlines(resolution="50m", color="black")
ax.gridlines(draw_labels=True, linestyle="--")

# 自定义色带
ocean_colors = [
    "#f4fdfe",
    "#c4edfa",
    "#94dff6",
    "#63cbee",
    "#4a91cb",
    "#2f56a9",
    "#17208b",
    "#0a017a",
    "#0b007a",
    "#0c075f",
]
custom_cmap = mcolors.LinearSegmentedColormap.from_list(
    "custom_ocean", ocean_colors, N=256
)

with rasterio.open(dem_tif) as src:
    dem_data = src.read(1, masked=True)
    dem_data = -dem_data
    left, bottom, right, top = src.bounds
    extent = [left, right, bottom, top]

    im = ax.imshow(
        dem_data,
        extent=extent,
        transform=ccrs.PlateCarree(),
        origin="upper",
        cmap=custom_cmap,
        vmin=0,
        vmax=8000,
        alpha=0.8,
        interpolation="bilinear",
        zorder=0,
    )

# 添加DEM色带
cbar = fig.colorbar(
    im,
    ax=ax,
    orientation="horizontal",
    pad=0.04,
    aspect=40,
    shrink=0.6,
    extend="max",
)
cbar.set_ticks([0, 2000, 4000, 6000, 8000])
cbar.set_ticklabels(["0", "2", "4", "6", "8"])
cbar.ax.tick_params(
    labelsize=16,
    labelcolor="black",
    length=0,
)
cbar.set_label("Depth (km)", fontsize=18)

# 添加标题并保存
title = "spilhaus_dem"
plt.title(title, fontsize=20)
plt.savefig(
    f"../fig_res/{title}.png",
    dpi=100,
    bbox_inches="tight",
)
print("ok")
