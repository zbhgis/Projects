"""
-------------------------------------------------------------------------------
@Author         :  zbhgis
@Github         :  https://github.com/zbhgis
@Description    :  different views of orthographic projection
-------------------------------------------------------------------------------
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 设置投影名称与对应的投影
projections = [
    ("orthographic (0, 0, 0)", ccrs.Orthographic()),
    ("orthographic (100, 40, 0)", ccrs.Orthographic(100, 40, 0)),
    ("orthographic (-100, 40, 0)", ccrs.Orthographic(-100, 40, 0)),
    ("orthographic (100, 40, 45)", ccrs.Orthographic(100, 40, 45)),
    ("orthographic (100, 40, 90)", ccrs.Orthographic(100, 40, 90)),
    ("orthographic (0, 90, 0)", ccrs.Orthographic(0, 90, 0)),
    ("orthographic (0, 90, 180)", ccrs.Orthographic(0, 90, 180)),
]

# 每个投影一张图片
for proj_name, proj in projections:
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.add_feature(cfeature.OCEAN, facecolor="#1f77b4", zorder=0)
    ax.add_feature(cfeature.LAND, facecolor="none", edgecolor="none", zorder=1)
    ax.coastlines(resolution="50m", color="black")
    ax.gridlines(draw_labels=True, linestyle="--")
    ax.set_title(proj_name, fontsize=16, pad=10)

    print(proj_name)
    plt.savefig(
        f"../fig_res/{proj_name}.png",
        dpi=100,
        bbox_inches="tight",
    )
    plt.close(fig)
