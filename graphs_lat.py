import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from zpracovani import *

def vykresli(ax, data, xlabels, ylabels, vmin=None, vmax=None, cmap='RdBu_r', d=False):

    data = np.array(data)
    y = np.array(ylabels, dtype=float)
    x = np.arange(len(xlabels))

    X, Y = np.meshgrid(x, y)

    if d:
        limit = max(abs(vmin), abs(vmax))
        pcm = ax.pcolormesh(
            X, Y, data.T,
            cmap=cmap,
            vmin=-limit,
            vmax=limit,
            shading="auto"
        )
    else:
        pcm = ax.pcolormesh(
            X, Y, data.T,
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            shading="auto"
        )

    ax.set_ylabel("Latitude (°N)", fontsize=16)
    ax.tick_params(axis='y', labelsize=14)

    xticks = []
    xticklabels = []

    for i, label in enumerate(xlabels):
        day = datetime.strptime(label, "%d/%m/%Y").day

        if day in (1, 15) or i == len(xlabels) - 1:
            xticks.append(i)
            xticklabels.append(format_date_label(label))

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontsize=12, rotation=45)

    minor_xticks = list(range(len(xlabels)))
    ax.set_xticks(minor_xticks, minor=True)

    ax.tick_params(axis='x', which='minor', length=3, width=0.7)
    ax.tick_params(axis='x', which='major', length=7, width=1.2)

    return pcm


# --- nastavení ---
latitudes = [x for x in range(40, 85, 5)]
level = 0.1


# --- načtení dat ---
u_data, ti, lats = jawara_lat_mean("u", level, latitudes)
t_data, _, _ = jawara_lat_mean("t", level, latitudes)

u_data = np.array(u_data, dtype=float)
t_data = np.array(t_data, dtype=float)


# --- škály ---
vmin_temp = np.min(t_data)
vmax_temp = np.max(t_data)

u_limit = max(abs(np.min(u_data)), abs(np.max(u_data)))

vmin_wind = -u_limit
vmax_wind = u_limit


# --- graf ---
fig, axs = plt.subplots(2, 1, figsize=(16, 10))
axs = axs.flatten()


pcm1 = vykresli(
    axs[0],
    t_data,
    ti,
    lats,
    vmin=vmin_temp,
    vmax=vmax_temp,
    d=False
)

cbar1 = plt.colorbar(
    pcm1,
    ax=axs[0],
    orientation="vertical",
    fraction=0.046,
    pad=0.04,
    extend="both"
)

cbar1.set_label("Zonal mean temperature (K)", fontsize=14)


pcm2 = vykresli(
    axs[1],
    u_data,
    ti,
    lats,
    vmin=vmin_wind,
    vmax=vmax_wind,
    d=True
)

cbar2 = plt.colorbar(
    pcm2,
    ax=axs[1],
    orientation="vertical",
    fraction=0.046,
    pad=0.04,
    extend="both"
)

cbar2.set_label("Zonal mean zonal wind (m/s)", fontsize=14)


fig.suptitle(
    f"JAWARA zonal mean – {level} hPa\n{rok}",
    fontsize=20,
    weight="bold"
)

plt.tight_layout()
fig.savefig(f"graphs/{rok}_lat_{level}.png")
plt.close(fig)