"""
-------------------------------------------------------------------------------
@Author         :  zbhgis
@Github         :  https://github.com/zbhgis
@Description    :  paleomap without basemap
@Data           :  https://zenodo.org/records/5460860
-------------------------------------------------------------------------------
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr
import numpy as np
from matplotlib.colors import ListedColormap
from pathlib import Path
from scipy.ndimage import gaussian_filter

# 基本配置
plt.rcParams["font.family"] = "Arial"
nc_name = "paleo_6min_100Ma"
nc_file = Path(f"./data_res/{nc_name}.nc")

# 读取数据
ds = xr.open_dataset(nc_file)
data = ds["z"].values
lats = ds["latitude"].values
lons = ds["longitude"].values
ds.close()

# 陆地=1, 海洋=0
data_binary = (data > 0).astype(np.float32)

# 高斯平滑
sigma_list = [1, 2, 3, 4, 5]
for sigma in sigma_list:
    # 图幅和投影
    proj = ccrs.EqualEarth()
    fig = plt.figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_global()

    # 手动在左侧添加纬度标记，用默认的绘制容易出错
    gl = ax.gridlines(
        draw_labels=False,
        linewidth=0,
        alpha=0,
    )
    lat_nums = [-60, -30, 0, 30, 60]
    lat_labels = [
        "60°S     ",
        "30°S   ",
        "0° ",
        "30°N   ",
        "60°N     ",
    ]
    for lat_num, lat_label in zip(lat_nums, lat_labels):
        ax.text(
            -180,  # 标签的经度坐标
            lat_num,  # 标签纬度坐标
            lat_label,  # 增大与边界的距离
            transform=ccrs.PlateCarree(),
            fontsize=9,
            color="black",
            ha="right",
            va="center",
        )

    # 读取数据
    data_smooth = gaussian_filter(data_binary, sigma=sigma)
    threshold = 0.5
    data_final = (data_smooth >= threshold).astype(np.float32)
    data_masked = np.ma.masked_equal(data_final, 0)

    # 白色+灰色
    binary_cmap = ListedColormap(["white", "gray"])

    im = ax.imshow(
        data_masked,
        extent=[lons.min(), lons.max(), lats.min(), lats.max()],
        transform=ccrs.PlateCarree(),
        origin="upper",
        cmap=binary_cmap,
        vmin=0,
        vmax=1,
        interpolation="nearest",
    )

    ax.set_facecolor("white")

    title = f"paleomap_nobasemap_{sigma}"
    plt.title(title)
    output_path = Path(f"./fig_res/{title}.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        output_path,
        dpi=100,
        bbox_inches="tight",
    )
    plt.close()
print("ok")
