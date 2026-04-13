"""
-------------------------------------------------------------------------------
@Author         :  zbhgis
@Github         :  https://github.com/zbhgis
@Description    :  generate some map-projection plots
-------------------------------------------------------------------------------
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import time

# 计时
start_time = time.perf_counter()

# 设置投影名称与对应的投影
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

# 每个投影一张图片
for proj_name, proj in projections:
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=proj)

    ax.set_global()
    ax.stock_img()
    ax.add_feature(
        cfeature.COASTLINE,
        linewidth=0.8,
        edgecolor="white",
        alpha=0.8,
    )

    ax.gridlines(
        draw_labels=True,
        linewidth=0.5,
        color="gray",
        linestyle="--",
        alpha=0.7,
    )

    ax.set_title(proj_name, fontsize=16, pad=10)

    print(proj_name)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f"../fig_res/world_maps_{proj_name}.png", dpi=100, bbox_inches="tight")
    plt.close(fig)

end_time = time.perf_counter()
print(end_time - start_time)
