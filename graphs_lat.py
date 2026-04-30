import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from zpracovani import *

def vykresli(ax, data, xlabels, ylabels, vmin=None, vmax=None, cmap='RdBu_r', d=False):

    data = np.array(data)
    y = np.array(ylabels, dtype=float)
    x = np.arange(len(xlabels))

    if d:
        limit = max(abs(vmin), abs(vmax))
        cont = ax.contourf(
            x, y, data.T,
            cmap=cmap,
            vmin=-limit,
            vmax=limit,
            levels=500
        )
    else:
        cont = ax.contourf(
            x, y, data.T,
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            levels=500
        )

    ax.set_ylabel("Latitude (°N)", fontsize=16)
    ax.tick_params(axis='y', labelsize=14)

    xticks = []
    xticklabels = []

    center_local_idx = len(xlabels) // 2

    for i, label in enumerate(xlabels):
        # každých 7 dní relativně ke středu
        if (i - center_local_idx) % 7 == 0 or i == len(xlabels) - 1:
            xticks.append(i)
            xticklabels.append(format_date_label(label))

    # --- střední den ---
    center_local_idx = len(xlabels) // 2
    ax.axvline(center_local_idx, linestyle='--', linewidth=1)

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontsize=12, rotation=45)

    minor_xticks = list(range(len(xlabels)))
    ax.set_xticks(minor_xticks, minor=True)

    ax.tick_params(axis='x', which='minor', length=3, width=0.7)
    ax.tick_params(axis='x', which='major', length=7, width=1.2)

    return cont

def get_closest_lat(lat_choice, lats, t_data, u_data):
    lats_array = np.array(lats, dtype=float)
    idx = np.argmin(np.abs(lats_array - lat_choice))
    lat_real = lats_array[idx]
    lat_display = round(lat_real)

    t_line = t_data[:, idx]
    u_line = u_data[:, idx]

    return idx, lat_real, lat_display, t_line, u_line

# --- nastavení ---
latitudes = [x for x in range(40, 85, 5)]
level = float(input("Zadejte tlakovou hladinu: "))
lat_choice1 = 60
lat_choice2 = 80
center_date = "22/01/2009"

# --- načtení dat ---
u_data, ti, lats = jawara_lat_mean("u", level, latitudes)
t_data, _, _ = jawara_lat_mean("t", level, latitudes)

u_data = np.array(u_data, dtype=float)
t_data = np.array(t_data, dtype=float)

# --- ořez časového období ---
center_idx = ti.index(center_date)

start = center_idx - 14
end = center_idx + 14 + 1  # +1 protože slice je exclusive

ti = ti[start:end]
t_data = t_data[start:end, :]
u_data = u_data[start:end, :]

# --- anomálie vůči prvním 14 dnům ---
t_ref = np.mean(t_data[:14, :], axis=0)
u_ref = np.mean(u_data[:14, :], axis=0)

t_anom = t_data - t_ref
u_anom = u_data - u_ref

t_lim = max(abs(np.min(t_anom)), abs(np.max(t_anom)))
u_lim_anom = max(abs(np.min(u_anom)), abs(np.max(u_anom)))

# --- výběr nejbližší latitude ---
_, lat1_real, lat1_disp, t1_line, u1_line = get_closest_lat(lat_choice1, lats, t_data, u_data)
_, lat2_real, lat2_disp, t2_line, u2_line = get_closest_lat(lat_choice2, lats, t_data, u_data)

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

sm = mpl.cm.ScalarMappable(
    norm=mpl.colors.Normalize(vmin=vmin_temp, vmax=vmax_temp),
    cmap='RdBu_r'
)

sm.set_array([])

cbar1 = plt.colorbar(
    sm,
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

sm = mpl.cm.ScalarMappable(
    norm=mpl.colors.Normalize(vmin=vmin_wind, vmax=vmax_wind),
    cmap='RdBu_r'
)

sm.set_array([])

cbar2 = plt.colorbar(
    sm,
    ax=axs[1],
    orientation="vertical",
    fraction=0.046,
    pad=0.04,
    extend="both"
)

cbar2.set_label("Zonal mean zonal wind (m/s)", fontsize=14)

fig.suptitle(
    f"JAWARA zonal mean – {level} hPa {rok}",
    fontsize=20,
    weight="bold"
)

plt.tight_layout()
fig.savefig(f"graphs_lat/{rok}_lat_{level}.png")
plt.close(fig)

fig, axs = plt.subplots(2, 1, figsize=(16, 10))
axs = axs.flatten()

# --- teplota anomálie ---
pcm1 = vykresli(
    axs[0],
    t_anom,
    ti,
    lats,
    vmin=-t_lim,
    vmax=t_lim,
    d=True
)

sm = mpl.cm.ScalarMappable(
    norm=mpl.colors.Normalize(vmin=-t_lim, vmax=t_lim),
    cmap='RdBu_r'
)
sm.set_array([])

cbar1 = plt.colorbar(
    sm,
    ax=axs[0],
    fraction=0.046,
    pad=0.04,
    extend="both"
)

cbar1.set_label("Temperature difference (K)", fontsize=14)

# --- vítr anomálie ---
pcm2 = vykresli(
    axs[1],
    u_anom,
    ti,
    lats,
    vmin=-u_lim_anom,
    vmax=u_lim_anom,
    d=True
)

sm = mpl.cm.ScalarMappable(
    norm=mpl.colors.Normalize(vmin=-u_lim_anom, vmax=u_lim_anom),
    cmap='RdBu_r'
)
sm.set_array([])

cbar2 = plt.colorbar(
    sm,
    ax=axs[1],
    fraction=0.046,
    pad=0.04,
    extend="both"
)

cbar2.set_label("Zonal wind difference (m/s) (m/s)", fontsize=14)

fig.suptitle(
    f"JAWARA zonal mean – {level} hPa {rok}",
    fontsize=20,
    weight="bold"
)

plt.tight_layout()
fig.savefig(f"graphs_lat/{rok}_lat_{level}_diff.png")
plt.close(fig)

fig, axs = plt.subplots(2, 1, figsize=(16, 10))

# --- teplota ---
axs[0].plot(ti, t1_line, label=f"{lat1_disp}°N")
axs[0].plot(ti, t2_line, label=f"{lat2_disp}°N")

axs[0].set_ylabel("Temperature (K)", fontsize=14)
axs[0].set_title("Temperature time series", fontsize=16)
axs[0].legend()

# --- vítr ---
axs[1].plot(ti, u1_line, label=f"{lat1_disp}°N")
axs[1].plot(ti, u2_line, label=f"{lat2_disp}°N")

axs[1].set_ylabel("Zonal wind (m/s)", fontsize=14)
axs[1].set_title("Zonal wind time series", fontsize=16)
axs[1].legend()


# --- osa x (stejná logika jako máš) ---
xticks = []
xticklabels = []

center_local_idx = len(ti) // 2

for i, label in enumerate(ti):
    if (i - center_local_idx) % 7 == 0 or i == len(ti) - 1:
        xticks.append(i)
        xticklabels.append(format_date_label(label))

center_local_idx = len(ti) // 2

for ax in axs:
    # major ticks (po 5 dnech)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontsize=12, rotation=45)

    # minor ticks (každý den)
    minor_xticks = list(range(len(ti)))
    ax.set_xticks(minor_xticks, minor=True)

    ax.tick_params(axis='x', which='minor', length=3, width=0.7)
    ax.tick_params(axis='x', which='major', length=7, width=1.2)

    # --- střední den ---
    ax.axvline(center_local_idx, linestyle='--', linewidth=1)

fig.suptitle(f"JAWARA Time series – {level} hPa {rok}", fontsize=20, weight="bold")

plt.tight_layout()
fig.savefig(f"graphs_lat/{rok}_timeseries_{level}.png")
plt.close(fig)