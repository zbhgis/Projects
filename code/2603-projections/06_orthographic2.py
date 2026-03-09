"""
-------------------------------------------------------------------------------
@Author         :  zbhgis
@Github         :  https://github.com/zbhgis
@Description    :  different extents of orthographic projection
-------------------------------------------------------------------------------
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.path as mpath
import matplotlib.ticker as mticker

extents = [60, 40, 20]

# 每个投影一张图片
for extent in extents:
    proj_name, proj = ("orthographic (0, 90, 0)", ccrs.Orthographic(0, 90, 0))
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=proj)

    ax.set_extent([-180, 180, extent, 90], crs=ccrs.PlateCarree())
    theta = np.linspace(0, 2 * np.pi, 100)
    center = (0.5, 0.5)
    radius = 0.5
    vertices = np.column_stack(
        [center[0] + radius * np.cos(theta), center[1] + radius * np.sin(theta)]
    )
    circle_path = mpath.Path(vertices)
    ax.set_boundary(circle_path, transform=ax.transAxes)

    ax.add_feature(cfeature.OCEAN, facecolor="#1f77b4", zorder=0)
    ax.add_feature(cfeature.LAND, facecolor="none", edgecolor="none", zorder=1)
    ax.coastlines(resolution="50m", color="black")
    gl = ax.gridlines(
        draw_labels=True,
        linestyle="--",
        alpha=0.5,
        linewidth=0.8,
    )
    gl.xlocator = mticker.MultipleLocator(20)
    gl.ylocator = mticker.MultipleLocator(20)
    ax.set_title(proj_name, fontsize=16, pad=10)

    print(proj_name)
    plt.savefig(
        f"./fig_res/{proj_name}_{extent}.png",
        dpi=100,
        bbox_inches="tight",
    )
    plt.close(fig)
