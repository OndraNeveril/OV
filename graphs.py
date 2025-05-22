from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

while True:
    rok = int(input("2002 nebo 2019? "))
    if rok in [2002, 2019]:
        break

def den_datum(den, rok, *p):
    prvni_den = datetime(rok, 1, 1)
    if p:
        cilovy_datum = prvni_den + timedelta(days=(den - 1) / 8)
    else:
        cilovy_datum = prvni_den + timedelta(days=den - 1)
    return cilovy_datum.strftime("%d/%m/%Y")

def datum_den(datum):
    dt = datetime.strptime(datum, "%d/%m/%Y")
    rok = int(datum[-4:])
    prvni_den = datetime(rok, 1, 1)
    rozdil = (dt.replace(year=rok) - prvni_den).days + 1
    return rozdil

def dates(s, inp, out, x):
    for i in range(len(inp.variables['valid_time'][:])):
        if (i + x) % 15 == 0:
            out.append(den_datum(datum_den(s) + i + x, rok))
    x += len(inp.variables['valid_time'][:])
    return out, x

def av(inp, out, x):
    for i in range(len(inp)):
        out.append([])
        for j in range(len(inp[0])):
            a = np.array(inp[i][j])
            b = np.mean(a)
            out[i + x].append(b)
    x += len(inp)
    return x, out

def prumeruj_po_8(data):
    n = len(data)
    nove_data = []
    for i in range(0, n, 8):
        blok = data[i:i+8]
        if len(blok) == 8:
            avg = np.mean(blok, axis=0)
            nove_data.append(avg)
    return np.array(nove_data)

def euf():
    folder = "./"
    if rok == 2019:
        files = ["eu6.nc", "eu7.nc", "eu8.nc", "eu9.nc"]
    if rok == 2002:
        files = ["eu208.nc", "eu209.nc", "eu210.nc", "eu211.nc"]
    data = []
    time_labels = []
    x = 0
    z = 0
    for f in files:
        dataset = Dataset(os.path.join(folder, f))
        var_data = dataset.variables['u'][:]
        pressure_levels = dataset.variables['pressure_level'][:]
        time_labels, z = dates(f"01/06/{rok}", dataset, time_labels, z)
        x, data = av(var_data, data, x)
    print("euf done")
    return data, time_labels, pressure_levels

def etf():
    folder = "./"
    if rok == 2019:
        files = ["et6.nc", "et7.nc", "et8.nc", "et9.nc"]
    if rok == 2002:
        files = ["et208.nc", "et209.nc", "et210.nc", "et211.nc"]
    data = []
    x = 0
    for f in files:
        dataset = Dataset(os.path.join(folder, f))
        var_data = dataset.variables['t'][:]
        x, data = av(var_data, data, x)
    print("etf done")
    return data

def muf():
    folder = "./Merra"
    files = sorted([f for f in os.listdir(folder) if f.endswith(".nc")], key=lambda x: int(x[1:].split('.')[0]))
    data = []
    x = 0
    z = 0
    for f in files:
        filepath = os.path.join(folder, f)
        dataset = Dataset(filepath)
        var_data = dataset.variables['U'][:]
        var_data = prumeruj_po_8(var_data)
        x, data = av(var_data, data, x)
    print("muf done")
    return data

def mtf():
    folder = "./Merra"
    files = sorted([f for f in os.listdir(folder) if f.endswith(".nc")], key=lambda x: int(x[1:].split('.')[0]))
    data = []
    x = 0
    for f in files:
        filepath = os.path.join(folder, f)
        dataset = Dataset(filepath)
        var_data = dataset.variables['T'][:]
        var_data = prumeruj_po_8(var_data)
        x, data = av(var_data, data, x)
    print("mtf done")
    return data

eu, ti, p = euf()
et = etf()
mu = muf()
mt = mtf()

eu_arr = np.array(eu)
mu_arr = np.array(mu)
et_arr = np.array(et)
mt_arr = np.array(mt)

eu_diff = eu_arr - mu_arr
et_diff = et_arr - mt_arr

fig, axs = plt.subplots(2, 2, figsize=(20, 12))
axs = axs.flatten()

def nastav_ose_x(ax, labels, total_len):
    xticklabels = ['' for _ in range(total_len)]
    for i in range(0, total_len, 15):
        if i // 15 < len(labels):
            xticklabels[i] = labels[i // 15]
    ax.set_xticks(range(total_len))
    ax.set_xticklabels(xticklabels, rotation=0)
    ax.set_xlabel("Time")

def nastav_ose_y(ax, labels, total_len):
    ax.set_yticks(range(total_len))
    ax.set_yticklabels(labels, rotation=0)

def vykresli(ax, data, title, xlabels, ylabels, vmin=None, vmax=None, cmap='coolwarm'):
    cont = ax.contourf(np.array(data).T, cmap=cmap, levels=16, vmin=vmin, vmax=vmax)
    ax.set_title(title)
    ax.set_ylabel("Pressure level (hPa)")
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels([xlabels[i // 15] if i % 15 == 0 and i // 15 < len(xlabels) else '' for i in range(len(data))])
    ax.set_yticks(range(len(ylabels)))
    ax.set_yticklabels(ylabels)
    return cont

vmin_wind = min(np.min(eu), np.min(mu))
vmax_wind = max(np.max(eu), np.max(mu))
vlim_diff_wind = np.max(np.abs(eu_diff))

vmin_temp = min(np.min(et), np.min(mt))
vmax_temp = max(np.max(et), np.max(mt))
vlim_diff_temp = np.max(np.abs(et_diff))

fig, axs = plt.subplots(2, 2, figsize=(20, 12))
axs = axs.flatten()

tituly = [
    "Zonal wind at SH from ERA5",
    "Zonal wind at SH from MERRA2",
    "Temperature at SH from ERA5",
    "Temperature at SH from MERRA2"
]
data_sady = [eu, mu, et, mt]
vmin_sady = [vmin_wind, vmin_wind, vmin_temp, vmin_temp]
vmax_sady = [vmax_wind, vmax_wind, vmax_temp, vmax_temp]

for ax, title, data, vmin_, vmax_ in zip(axs, tituly, data_sady, vmin_sady, vmax_sady):
    cbar = vykresli(ax, data, title, ti, p, vmin=vmin_, vmax=vmax_)
    fig.colorbar(cbar, ax=ax)

plt.tight_layout()
if rok == 2019:
    fig.savefig("vse_2019.png")
if rok == 2002:
    fig.savefig("vse_2002.png")
plt.close(fig)

fig_diff, axs_diff = plt.subplots(2, 1, figsize=(10, 12))
tituly_diff = [
    "ERA5 - MERRA2 Zonal wind difference",
    "ERA5 - MERRA2 Temperature difference"
]
data_diff = [eu_diff, et_diff]
vlims_diff = [vlim_diff_wind, vlim_diff_temp]

for ax, title, data, vlim in zip(axs_diff, tituly_diff, data_diff, vlims_diff):
    cbar = vykresli(ax, data, title, ti, p, vmin=-vlim, vmax=vlim, cmap='bwr')
    fig_diff.colorbar(cbar, ax=ax)

plt.tight_layout()
if rok == 2019:
    fig_diff.savefig("rem_2019.png")
if rok == 2002:
    fig_diff.savefig("rem_2002.png")
plt.close(fig_diff)