from netCDF4 import Dataset
import numpy as np
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

def format_date_label(date_str):
    dt = datetime.strptime(date_str, "%d/%m/%Y")
    return dt.strftime("%b\n%d")


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
        if rok == 2002:
            time_labels, z = dates(f"01/08/2002", dataset, time_labels, z)
        if rok == 2019:
            time_labels, z = dates(f"01/06/2019", dataset, time_labels, z)
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