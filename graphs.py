import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mticker
from datetime import datetime
from zpracovani import *

def vykresli(ax, data, title, xlabels, ylabels, yticks, index, ncols,
             vmin=None, vmax=None, cmap='RdBu_r', d=False):
    data = np.array(data)
    y = np.array(ylabels, dtype=float)
    x = np.arange(len(xlabels))

    # Kontury
    if d:
        cont = ax.contourf(x, y, data.T, cmap=cmap,
                           vmin=-max(abs(vmin), abs(vmax), 4),
                           vmax=max(abs(vmin), abs(vmax), 4),
                           levels=100)
    else:
        cont = ax.contourf(x, y, data.T, cmap=cmap,
                           vmin=vmin,
                           vmax=vmax,
                           levels=100)

    # Logaritmická osa Y
    ax.set_yscale('log')
    ax.invert_yaxis()
    ax.yaxis.set_major_locator(mticker.FixedLocator(yticks))
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.set_minor_locator(mticker.NullLocator())
    ax.tick_params(axis='y', labelsize=14)

    col = index % ncols
    row = index // ncols

    # Y osa jen levé sloupce
    if col == 0:
        ax.set_ylabel("Pressure level (hPa)", fontsize=16)
        ax.set_yticks(yticks)
        ax.set_yticklabels([f"{val:.1f}" for val in yticks])
    else:
        # pravé sloupce žádné Y tick labels
        ax.set_yticks(yticks)
        ax.set_yticklabels([])

    # X osa
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

    # Titulky datasetů
    if row == 0:
        ax.set_title(title, fontsize=16, weight='bold')

    # Colorbar pro pravé sloupce
    if col != 0:
        sm = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=vmin, vmax=vmax), cmap=cmap)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, extend='both', orientation='vertical',
                            fraction=0.046, pad=0.04)
        if d:
            cbar.set_label("Zonal mean zonal wind (m/s)", fontsize=14)
        else:
            cbar.set_label("Zonal mean temperature (K)", fontsize=14)

    return cont


# --- Hlavní část ---
datasets_list = [
    ("MERRA2", muf, mtf),
    ("JAWARA", wuf, wtf)
]

results = []

for name, fu, ft in datasets_list:
    u_data, ti, p = fu()
    t_data, _, _ = ft()

    u_data = np.array(u_data, dtype=float)
    t_data = np.array(t_data, dtype=float)

    results.append({
        "name": name,
        "u": u_data,
        "t": t_data,
        "time": ti,
        "pressure": p
    })

vmin_temp = min(np.min(r["t"]) for r in results)
vmax_temp = max(np.max(r["t"]) for r in results)
vmin_wind = min(np.min(r["u"]) for r in results)
vmax_wind = max(np.max(r["u"]) for r in results)

n = len(results)
fig, axs = plt.subplots(2, n, figsize=(8*n, 12))

if n == 1:
    axs = np.array([[axs[0]], [axs[1]]])

axs = axs.flatten()

for i, r in enumerate(results):
    full_pressure = np.array(r["pressure"], dtype=float)
    yticks = full_pressure[(full_pressure <= 103) & (full_pressure >= 0.3)]
    yticks = yticks[::4]
    ytick_indices = [j for j, val in enumerate(full_pressure) if val in yticks]

    t_data_sel = r["t"][:, ytick_indices]
    u_data_sel = r["u"][:, ytick_indices]

    # levý horní graf: T
    vykresli(
        axs[i],
        t_data_sel,
        f"{chr(97+i)}) {r['name']}",
        r["time"],
        full_pressure[ytick_indices],
        full_pressure[ytick_indices],
        index=i,
        ncols=n,
        vmin=vmin_temp,
        vmax=vmax_temp,
        d=False
    )

    # pravý dolní graf: U
    vykresli(
        axs[i+n],
        u_data_sel,
        "",
        r["time"],
        full_pressure[ytick_indices],
        full_pressure[ytick_indices],
        index=i+n,
        ncols=n,
        vmin=vmin_wind,
        vmax=vmax_wind,
        d=True
    )

fig.suptitle(f"SSW Northern hemisphere {rok} - {rok + 1} winter\n", fontsize=20, weight='bold')
plt.tight_layout()
fig.savefig(f"graphs/{rok}.png")
plt.close(fig)