"""
-------------------------------------------------------------------------------
@Author         :  zbhgis
@Github         :  https://github.com/zbhgis
@Description    :  spilhaus without basemap
-------------------------------------------------------------------------------
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


fig = plt.figure(figsize=(10, 10), dpi=100)
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Spilhaus())
ax.set_global()
ax.add_feature(cfeature.OCEAN, facecolor="#1f77b4", zorder=0)
ax.add_feature(cfeature.LAND, facecolor="none", edgecolor="none", zorder=1)
ax.coastlines(resolution="50m", color="black")
ax.gridlines(draw_labels=True, linestyle="--")

title = "spilhaus_nobasemap"
plt.title(title)
plt.savefig(
    f"../fig_res/{title}.png",
    dpi=100,
    bbox_inches="tight",
)
print("ok")
