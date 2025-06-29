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
    try:
        for i in range(len(inp.variables['valid_time'][:])):
            if (i + x) % 15 == 0:
                out.append(den_datum(datum_den(s) + i + x, rok))
        x += len(inp.variables['valid_time'][:])
    except KeyError:
        for i in range(len(inp.variables['time'][:])):
            if (i + x) % 15 == 0:
                out.append(den_datum(datum_den(s) + i + x, rok))
        x += len(inp.variables['time'][:])
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

def prumeruj_po_4(data):
    n = data.shape[0]
    nove_data = []
    for i in range(0, n, 4):
        blok = data[i:i+4]
        if blok.shape[0] == 4:
            avg = np.mean(blok, axis=0)
            nove_data.append(avg)
    return np.array(nove_data)

def euf():
    folder = "./Era_2019" if rok == 2019 else "./Era_2002"
    files = ["eu6.nc", "eu7.nc", "eu8.nc", "eu9.nc"] if rok == 2019 else ["eu208.nc", "eu209.nc", "eu210.nc", "eu211.nc"]
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
    return data, time_labels, pressure_levels

def etf():
    folder = "./Era_2019" if rok == 2019 else "./Era_2002"
    files = ["et6.nc", "et7.nc", "et8.nc", "et9.nc"] if rok == 2019 else ["et208.nc", "et209.nc", "et210.nc", "et211.nc"]
    data = []
    x = 0
    for f in files:
        dataset = Dataset(os.path.join(folder, f))
        var_data = dataset.variables['t'][:]
        x, data = av(var_data, data, x)
    return data

def muf():
    folder = "./Merra_2019" if rok == 2019 else "./Merra_2002"
    files = sorted([f for f in os.listdir(folder) if f.endswith(".nc")], key=lambda x: int(x[1:].split('.')[0]))
    data = []
    x = 0
    for f in files:
        dataset = Dataset(os.path.join(folder, f))
        var_data = prumeruj_po_8(dataset.variables['U'][:])
        x, data = av(var_data, data, x)
    return data

def mtf():
    folder = "./Merra_2019" if rok == 2019 else "./Merra_2002"
    files = sorted([f for f in os.listdir(folder) if f.endswith(".nc")], key=lambda x: int(x[1:].split('.')[0]))
    data = []
    x = 0
    for f in files:
        dataset = Dataset(os.path.join(folder, f))
        var_data = prumeruj_po_8(dataset.variables['T'][:])
        x, data = av(var_data, data, x)
    return data

def juf():
    folder = "./Jra_2019" if rok == 2019 else "./Jra_2002"
    files = ["ju6.nc", "ju7.nc", "ju8.nc", "ju9.nc"] if rok == 2019 else ["ju208.nc", "ju209.nc", "ju210.nc", "ju211.nc"]
    data = []
    time_labels = []
    x = 0
    z = 0
    vybrane_tlaky = [100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1]
    for f in files:
        with Dataset(os.path.join(folder, f)) as dataset:
            all_pressures = dataset.variables['pressure_level'][:]
            indexy = [i for i, p in enumerate(all_pressures) if p in vybrane_tlaky]
            indexy = sorted(indexy, key=lambda i: vybrane_tlaky.index(all_pressures[i]))
            var_data = prumeruj_po_4(dataset.variables['ugrd-pres-an-ll125'][:])
            vybrana_data = var_data[:, indexy, :, :]
            time_labels, z = dates(f"01/06/{rok}", dataset, time_labels, z)
            x, data = av(vybrana_data, data, x)
            pressure_levels = all_pressures[indexy]
    return np.array(data), time_labels, pressure_levels

def jtf():
    folder = "./Jra_2019" if rok == 2019 else "./Jra_2002"
    files = ["jt6.nc", "jt7.nc", "jt8.nc", "jt9.nc"] if rok == 2019 else ["jt208.nc", "jt209.nc", "jt210.nc", "jt211.nc"]
    data = []
    x = 0
    vybrane_tlaky = [100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1]
    for f in files:
        with Dataset(os.path.join(folder, f)) as dataset:
            all_pressures = dataset.variables['pressure_level'][:]
            indexy = [i for i, p in enumerate(all_pressures) if p in vybrane_tlaky]
            indexy = sorted(indexy, key=lambda i: vybrane_tlaky.index(all_pressures[i]))
            var_data = prumeruj_po_4(dataset.variables['tmp-pres-an-ll125'][:])
            vybrana_data = var_data[:, indexy, :, :]
            x, data = av(vybrana_data, data, x)
    return np.array(data)

def vykresli(ax, data, title, xlabels, ylabels, vmin=None, vmax=None, cmap='coolwarm'):
    cont = ax.contourf(np.array(data).T, cmap=cmap, levels=16, vmin=vmin, vmax=vmax)
    ax.set_title(title)
    ax.set_ylabel("Pressure level (hPa)")
    ax.set_xlabel("Time (dates every 15 days)")
    ax.set_xticks(range(len(data)))
    max_label_index = len(xlabels) * 15
    ax.set_xticks(range(min(len(data), max_label_index)))
    ax.set_xticklabels([xlabels[i // 15] if i % 15 == 0 and i // 15 < len(xlabels) else '' for i in range(min(len(data), max_label_index))])
    ax.set_yticks(range(len(ylabels)))
    ax.set_yticklabels(ylabels)
    return cont

eu, ti, p = euf()
et = etf()
mu = muf()
mt = mtf()
ju, _, _ = juf()
jt = jtf()

eu_arr = np.array(eu)
mu_arr = np.array(mu)
et_arr = np.array(et)
mt_arr = np.array(mt)

eu_mu_diff = eu_arr - mu_arr
eu_ju_diff = eu_arr - ju
mu_ju_diff = mu_arr - ju

et_mt_diff = et_arr - mt_arr
et_jt_diff = et_arr - jt
mt_jt_diff = mt_arr - jt

vmin_wind = min(np.min(eu_arr), np.min(mu_arr), np.min(ju))
vmax_wind = max(np.max(eu_arr), np.max(mu_arr), np.max(ju))
vmin_temp = min(np.min(et_arr), np.min(mt_arr), np.min(jt))
vmax_temp = max(np.max(et_arr), np.max(mt_arr), np.max(jt))

fig, axs = plt.subplots(2, 3, figsize=(36, 12))
axs = axs.flatten()

tituly = [
    "Zonal wind at SH from ERA5",
    "Zonal wind at SH from MERRA2",
    "Zonal wind at SH from JRA",
    "Temperature at SH from ERA5",
    "Temperature at SH from MERRA2",
    "Temperature at SH from JRA"
]

data_sady = [eu_arr, mu_arr, ju, et_arr, mt_arr, jt]
vmin_sady = [vmin_wind]*3 + [vmin_temp]*3
vmax_sady = [vmax_wind]*3 + [vmax_temp]*3

for ax, title, data, vmin_, vmax_ in zip(axs, tituly, data_sady, vmin_sady, vmax_sady):
    cbar = vykresli(ax, data, title, ti, p, vmin=vmin_, vmax=vmax_)
    fig.colorbar(cbar, ax=ax)

plt.tight_layout()
fig.savefig(f"All_{rok}.png")
plt.close(fig)

fig_all_diff, axs_all = plt.subplots(2, 3, figsize=(36, 12))
axs_all = axs_all.flatten()

tituly_diff_all = [
    "Difference between ERA5 - MERRA2 Zonal Wind",
    "Difference between ERA5 - JRA Zonal Wind",
    "Difference between MERRA2 - JRA Zonal Wind",
    "Difference between ERA5 - MERRA2 Temperature",
    "Difference between ERA5 - JRA Temperature",
    "Difference between MERRA2 - JRA Temperature"
]

data_diff_all = [eu_mu_diff, eu_ju_diff, mu_ju_diff, et_mt_diff, et_jt_diff, mt_jt_diff]
vlims_diff = [np.max(np.abs(d)) for d in data_diff_all]

for ax, title, data, vlim in zip(axs_all, tituly_diff_all, data_diff_all, vlims_diff):
    cbar = vykresli(ax, data, title, ti, p, vmin=-vlim, vmax=vlim, cmap='bwr')
    fig_all_diff.colorbar(cbar, ax=ax)

plt.tight_layout()
fig_all_diff.savefig(f"All_differences_{rok}.png")
plt.close(fig_all_diff)

detailni_indexy = [i for i, hladina in enumerate(p) if 1 <= hladina <= 10]

def vyber_detailni_hladiny(data, indexy):
    data_np = np.array(data)
    if data_np.ndim == 3:
        return data_np[:, indexy, :, :]
    elif data_np.ndim == 2:
        return data_np[:, indexy]
    else:
        return data_np

detail_eu = vyber_detailni_hladiny(eu_arr, detailni_indexy)
detail_mu = vyber_detailni_hladiny(mu_arr, detailni_indexy)
detail_ju = vyber_detailni_hladiny(ju, detailni_indexy)
detail_et = vyber_detailni_hladiny(et_arr, detailni_indexy)
detail_mt = vyber_detailni_hladiny(mt_arr, detailni_indexy)
detail_jt = vyber_detailni_hladiny(jt, detailni_indexy)

detail_eu_mu_diff = detail_eu - detail_mu
detail_eu_ju_diff = detail_eu - detail_ju
detail_mu_ju_diff = detail_mu - detail_ju
detail_et_mt_diff = detail_et - detail_mt
detail_et_jt_diff = detail_et - detail_jt
detail_mt_jt_diff = detail_mt - detail_jt

detail_p = [p[i] for i in detailni_indexy]

detail_vmin_wind = min(np.min(detail_eu), np.min(detail_mu), np.min(detail_ju))
detail_vmax_wind = max(np.max(detail_eu), np.max(detail_mu), np.max(detail_ju))
detail_vmin_temp = min(np.min(detail_et), np.min(detail_mt), np.min(detail_jt))
detail_vmax_temp = max(np.max(detail_et), np.max(detail_mt), np.max(detail_jt))

fig_detail, axs_detail = plt.subplots(2, 3, figsize=(36, 12))
axs_detail = axs_detail.flatten()

tituly_detail = [
    "Zonal wind at SH from ERA5 (detailed 1 - 10 hPa)",
    "Zonal wind at SH from MERRA2 (detailed 1 - 10 hPa)",
    "Zonal wind at SH from JRA (detailed 1 - 10 hPa)",
    "Temperature at SH from ERA5 (detailed 1 - 10 hPa)",
    "Temperature at SH from MERRA2 (detailed 1 - 10 hPa)",
    "Temperature at SH from JRA (detailed 1 - 10 hPa)"
]

data_sady_detail = [detail_eu, detail_mu, detail_ju, detail_et, detail_mt, detail_jt]
vmin_sady_detail = [detail_vmin_wind]*3 + [detail_vmin_temp]*3
vmax_sady_detail = [detail_vmax_wind]*3 + [detail_vmax_temp]*3

for ax, title, data, vmin_, vmax_ in zip(axs_detail, tituly_detail, data_sady_detail, vmin_sady_detail, vmax_sady_detail):
    cbar = vykresli(ax, data, title, ti, detail_p, vmin=vmin_, vmax=vmax_)
    fig_detail.colorbar(cbar, ax=ax)

plt.tight_layout()
fig_detail.savefig(f"All_detailed_1_10_{rok}.png")
plt.close(fig_detail)

fig_detail_diff, axs_detail_diff = plt.subplots(2, 3, figsize=(36, 12))
axs_detail_diff = axs_detail_diff.flatten()

tituly_diff_detail = [
    "Difference between ERA5 - MERRA2 Zonal Wind (detailed 1 - 10 hPa)",
    "Difference between ERA5 - JRA Zonal Wind (detailed 1 - 10 hPa)",
    "Difference between MERRA2 - JRA Zonal Wind (detailed 1 - 10 hPa)",
    "Difference between ERA5 - MERRA2 Temperature (detailed 1 - 10 hPa)",
    "Difference between ERA5 - JRA Temperature (detailed 1 - 10 hPa)",
    "Difference between MERRA2 - JRA Temperature (detailed 1 - 10 hPa)"
]

data_diff_detail = [detail_eu_mu_diff, detail_eu_ju_diff, detail_mu_ju_diff,
                    detail_et_mt_diff, detail_et_jt_diff, detail_mt_jt_diff]
vlims_diff_detail = [np.max(np.abs(d)) for d in data_diff_detail]

for ax, title, data, vlim in zip(axs_detail_diff, tituly_diff_detail, data_diff_detail, vlims_diff_detail):
    cbar = vykresli(ax, data, title, ti, detail_p, vmin=-vlim, vmax=vlim, cmap='bwr')
    fig_detail_diff.colorbar(cbar, ax=ax)

plt.tight_layout()
fig_detail_diff.savefig(f"All_differences_detailed_1_10_{rok}.png")
plt.close(fig_detail_diff)