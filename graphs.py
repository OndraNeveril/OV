from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

def den_datum(den, rok, *p):
    prvni_den = datetime(rok, 1, 1)
    if p:
        cilovy_datum = prvni_den + timedelta(days=den - 1)/8
    else:
        cilovy_datum = prvni_den + timedelta(days=den - 1)
    return cilovy_datum.strftime("%d/%m/%Y")

def datum_den(datum):
    dt = datetime.strptime(datum, "%d/%m/%Y")
    rok = int(datum[-4:])
    prvni_den = datetime(rok, 1, 1)
    rozdil = (dt.replace(year=rok) - prvni_den).days + 1
    return rozdil

def dates(s, inp, out, *p):
    x = len(out)
    if p:
        for i in range(len(inp.variables['time'][:])):
            if (i + x) % 150 == 0:
                out.append(den_datum(datum_den(s) + i + x, 2019))
    else:
        for i in range(len(inp.variables['valid_time'][:])):
            if (i + x) % 15 == 0:
                out.append(den_datum(datum_den(s) + i + x, 2019))
    return out

def av(inp, out, x):
    for i in range(len(inp)):
        out.append([])
        for j in range(len(inp[0])):
            a = np.array(inp[i][j])
            b = np.mean(a)
            out[i + x].append(b)
        print(x + i)
    x += len(inp)
    return x, out

def euf():
    eu6 = Dataset('eu6.nc')
    eu7 = Dataset('eu7.nc')
    eu8 = Dataset('eu8.nc')
    eu9 = Dataset('eu9.nc')

    eu6_2 = eu6.variables['u']
    eu7_2 = eu7.variables['u']
    eu8_2 = eu8.variables['u']
    eu9_2 = eu9.variables['u']

    p = [x for x in eu6.variables['pressure_level'][:]]
    ti = []
    ti = dates("01/06/2019", eu6, ti)
    ti = dates("01/07/2019", eu7, ti)
    ti = dates("01/08/2019", eu8, ti)
    ti = dates("01/09/2019", eu9, ti)

    eu = []
    x = 0

    x, eu = av(eu6_2, eu, x)
    x, eu = av(eu7_2, eu, x)
    x, eu = av(eu8_2, eu, x)
    x, eu = av(eu9_2, eu, x)

    return eu, ti, p

def etf():
    et6 = Dataset('et6.nc')
    et7 = Dataset('et7.nc')
    et8 = Dataset('et8.nc')
    et9 = Dataset('et9.nc')

    et6_2 = et6.variables['t']
    et7_2 = et7.variables['t']
    et8_2 = et8.variables['t']
    et9_2 = et9.variables['t']

    et = []
    x = 0

    x, et = av(et6_2, et, x)
    x, et = av(et7_2, et, x)
    x, et = av(et8_2, et, x)
    x, et = av(et9_2, et, x)

    return et

def muf():
    folder = "/media/ondrej/f33d1d42-ade5-41fb-98df-bd6fefb6cf63/dokument/AV/2025 - stratosferické ohřevy/Merra"
    files = sorted([f for f in os.listdir("/media/ondrej/f33d1d42-ade5-41fb-98df-bd6fefb6cf63/dokument/AV/2025 - stratosferické ohřevy/Merra") if f.endswith(".nc")], key=lambda x: int(x[1:].split('.')[0]))
    data = []
    time_labels = []
    x = 0

    for f in files:
        filepath = os.path.join(folder, f)
        dataset = Dataset(filepath)
        var_data = dataset.variables['U'][:]
        pressure_levels = dataset.variables['lev'][:]
        time_labels = dates("01/06/2019", dataset, time_labels, True)
        x, data = av(var_data, data, x)

    return data, time_labels, pressure_levels

def mtf():
    folder = "/media/ondrej/f33d1d42-ade5-41fb-98df-bd6fefb6cf63/dokument/AV/2025 - stratosferické ohřevy/Merra"
    files = sorted([f for f in os.listdir("/media/ondrej/f33d1d42-ade5-41fb-98df-bd6fefb6cf63/dokument/AV/2025 - stratosferické ohřevy/Merra") if f.endswith(".nc")], key=lambda x: int(x[1:].split('.')[0]))
    data = []
    x = 0

    for f in files:
        filepath = os.path.join(folder, f)
        dataset = Dataset(filepath)
        var_data = dataset.variables['T'][:]
        x, data = av(var_data, data, x)

    return data

eu, ti, p = euf()
et = etf()
mu, ti2, p2 = muf()
mt = mtf()

fig, axs = plt.subplots(2, 2, figsize=(20, 12))
axs = axs.flatten()

axs[0].contourf(list(map(list, zip(*eu))), cmap='coolwarm', levels=16)
axs[0].set_title('Zonal wind at Southern Hemisphere from ERA5')
axs[0].set_ylabel("Pressure level (hPa)")
axs[0].set_xticklabels(ti)
axs[0].set_yticklabels(p)

axs[1].contourf(list(map(list, zip(*mu))), cmap='coolwarm', levels=16)
axs[1].set_title('Zonal wind at Southern Hemisphere from MERRA2')
axs[1].set_ylabel("Pressure level (hPa)")
axs[1].set_xticklabels(ti2)
axs[1].set_yticklabels(p2)

axs[2].contourf(list(map(list, zip(*et))), cmap='coolwarm', levels=16)
axs[2].set_title('Temperature at Southern Hemisphere from ERA5')
axs[2].set_ylabel("Pressure level (hPa)")
axs[2].set_xticklabels(ti)
axs[2].set_yticklabels(p)

axs[3].contourf(list(map(list, zip(*mt))), cmap='coolwarm', levels=16)
axs[3].set_title('Zonal wind at Southern Hemisphere from MERRA2')
axs[3].set_ylabel("Pressure level (hPa)")
axs[3].set_xticklabels(ti2)
axs[3].set_yticklabels(p2)

plt.tight_layout()
plt.show()