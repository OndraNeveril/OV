from netCDF4 import Dataset
import numpy as np
import os
from datetime import datetime, timedelta

# --- výběr roku ---
while True:
    rok = int(input("Který rok? "))
    if rok in [2008, 2012, 2014, 2019]:
        break

# --- Funkce pro datum ---
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
            out.append(den_datum(datum_den(s) + i + x, rok))
        x += len(inp.variables['valid_time'][:])
    except KeyError:
        for i in range(len(inp.variables['time'][:])):
            out.append(den_datum(datum_den(s) + i + x, rok))
        x += len(inp.variables['time'][:])
    return out, x

# --- Pomocná funkce av() ---
def av(inp, out, x):
    """
    Agreguje a průměruje data přes vnitřní dimenze (např. lat/lon)
    a přidává je do seznamu out. Vrací aktualizovaný index a out.
    """
    for i in range(len(inp)):
        out.append([])
        for j in range(len(inp[0])):
            a = np.array(inp[i][j])
            b = np.mean(a)
            out[i + x].append(b)
    x += len(inp)
    return x, out

# --- Funkce pro průměrování po 8 a 4 ---
def prumeruj_po_8(data):
    n = data.shape[0] // 8
    data = data[:n*8]
    return data.reshape(n, 8, *data.shape[1:]).mean(axis=1)

def prumeruj_po_4(data):
    n = data.shape[0]
    nove_data = []
    for i in range(0, n, 4):
        blok = data[i:i+4]
        if blok.shape[0] == 4:
            nove_data.append(np.mean(blok, axis=0))
    return np.array(nove_data)

# --- Výběr šířky ---
def vyber_sirky(dataset):
    for key in ['latitude', 'lat']:
        if key in dataset.variables:
            sirky = dataset.variables[key][:]
            break
    else:
        raise KeyError("Latitude variable not found")
    indexy = np.where((sirky >= -90) & (sirky <= -60))[0]
    return indexy

# --- ERA funkce ---
def euf():
    folder = "./Era_2019" if rok == 2019 else "./Era_2002"
    files = ["eu6.nc","eu7.nc","eu8.nc","eu9.nc"] if rok == 2019 else ["eu208.nc","eu209.nc","eu210.nc","eu211.nc"]
    data, time_labels = [], []
    x = z = 0
    for f in files:
        dataset = Dataset(os.path.join(folder, f))
        lat_idx = vyber_sirky(dataset)
        var_data = dataset.variables['u'][:, :, lat_idx, :]
        var_data = np.mean(var_data, axis=(2,3))
        start_date = "01/06/2019" if rok == 2019 else "01/08/2002"
        time_labels, z = dates(start_date, dataset, time_labels, z)
        data.extend(var_data)
        pressure_levels = dataset.variables['pressure_level'][:].astype(int)
    return np.array(data), time_labels, pressure_levels

def etf():
    folder = "./Era_2019" if rok == 2019 else "./Era_2002"
    files = ["et6.nc","et7.nc","et8.nc","et9.nc"] if rok == 2019 else ["et208.nc","et209.nc","et210.nc","et211.nc"]
    data, time_labels = [], []
    x = z = 0
    for f in files:
        dataset = Dataset(os.path.join(folder, f))
        lat_idx = vyber_sirky(dataset)
        var_data = dataset.variables['t'][:, :, lat_idx, :]
        var_data = np.mean(var_data, axis=(2,3))
        start_date = "01/06/2019" if rok == 2019 else "01/08/2002"
        time_labels, z = dates(start_date, dataset, time_labels, z)
        data.extend(var_data)
        pressure_levels = dataset.variables['pressure_level'][:].astype(int)
    return np.array(data), time_labels, pressure_levels

# --- MERRA ---
def muf():
    folder = f"./Merra2/m{rok}"
    files = sorted(
        [f for f in os.listdir(folder) if f.endswith(".nc")],
        key=lambda x: int(x.split(".")[0][1:])
    )

    data = []
    time_labels = []
    z = 0
    start = f"01/09/{rok}"

    for f in files:
        dataset = Dataset(os.path.join(folder, f))
        var_data = dataset.variables['U'][:]
        var_data = prumeruj_po_8(var_data)
        var_data = np.mean(var_data, axis=(2,3))
        data.extend(var_data)

        for i in range(var_data.shape[0]):
            time_labels.append(den_datum(datum_den(start) + z + i, rok))

        z += var_data.shape[0]

        pressure_levels = dataset.variables['lev'][:]

    return np.array(data), time_labels, pressure_levels

def mtf():
    folder = f"./Merra2/m{rok}"
    files = sorted(
        [f for f in os.listdir(folder) if f.endswith(".nc")],
        key=lambda x: int(x.split(".")[0][1:])
    )

    data = []
    time_labels = []
    z = 0
    start = f"01/09/{rok}"

    for f in files:
        dataset = Dataset(os.path.join(folder, f))

        var_data = dataset.variables['T'][:]
        var_data = prumeruj_po_8(var_data)
        var_data = np.mean(var_data, axis=(2,3))

        data.extend(var_data)

        for i in range(var_data.shape[0]):
            time_labels.append(den_datum(datum_den(start) + z + i, rok))

        z += var_data.shape[0]

        pressure_levels = dataset.variables['lev'][:]

    return np.array(data), time_labels, pressure_levels

# --- JRA ---
def juf():
    folder = "./Jra_2019" if rok == 2019 else "./Jra_2002"
    files = ["ju6.nc","ju7.nc","ju8.nc","ju9.nc"] if rok == 2019 else ["ju208.nc","ju209.nc","ju210.nc","ju211.nc"]
    data, time_labels = [], []
    x = z = 0
    vybrane_tlaky = [100,70,50,30,20,10,7,5,3,2,1]
    for f in files:
        dataset = Dataset(os.path.join(folder, f))
        lat_idx = vyber_sirky(dataset)
        all_pressures = dataset.variables['pressure_level'][:]
        indexy = [i for i, p in enumerate(all_pressures) if p in vybrane_tlaky]
        indexy = sorted(indexy, key=lambda i: vybrane_tlaky.index(all_pressures[i]))
        var_data = prumeruj_po_4(dataset.variables['ugrd-pres-an-ll125'][:, :, lat_idx, :])
        var_data = np.mean(var_data, axis=(2,3))
        vybrana_data = var_data[:, indexy]
        data.extend(vybrana_data)
        time_labels, z = dates(f"01/06/{rok}", dataset, time_labels, z)
        pressure_levels = all_pressures[indexy]
    return np.array(data), time_labels, pressure_levels

def jtf():
    folder = "./Jra_2019" if rok == 2019 else "./Jra_2002"
    files = ["jt6.nc","jt7.nc","jt8.nc","jt9.nc"] if rok == 2019 else ["jt208.nc","jt209.nc","jt210.nc","jt211.nc"]
    data, time_labels = [], []
    x = z = 0
    vybrane_tlaky = [100,70,50,30,20,10,7,5,3,2,1]
    for f in files:
        dataset = Dataset(os.path.join(folder, f))
        lat_idx = vyber_sirky(dataset)
        all_pressures = dataset.variables['pressure_level'][:]
        indexy = [i for i, p in enumerate(all_pressures) if p in vybrane_tlaky]
        indexy = sorted(indexy, key=lambda i: vybrane_tlaky.index(all_pressures[i]))
        var_data = prumeruj_po_4(dataset.variables['tmp-pres-an-ll125'][:, :, lat_idx, :])
        var_data = np.mean(var_data, axis=(2,3))
        vybrana_data = var_data[:, indexy]
        data.extend(vybrana_data)
        time_labels, z = dates(f"01/06/{rok}", dataset, time_labels, z)
        pressure_levels = all_pressures[indexy]
    return np.array(data), time_labels, pressure_levels

# --- JAWARA ---
def wuf():
    folder = f"./Jawara/j{rok}"
    files = sorted([f for f in os.listdir(folder) if f.startswith("U") and f.endswith(".nc")])
    data, time_labels = [], []
    z = 0

    tlak_max = 103.0
    tlak_min = 0.3

    for f in files:
        dataset = Dataset(os.path.join(folder, f))

        # vyber šířky
        sirky = dataset.variables['latitude'][:] if 'latitude' in dataset.variables else dataset.variables['lat'][:]
        lat_idx = np.where((sirky >= 60) & (sirky <= 90))[0]

        # vyber hladin podle tlaku
        all_pressures = dataset.variables['level'][:].astype(float)
        level_idx = np.where((all_pressures <= tlak_max) & (all_pressures >= tlak_min))[0]
        pressure_levels = all_pressures[level_idx]

        # vybraná data a průměr přes lat/lon
        var_data = dataset.variables['u'][:, level_idx, lat_idx, :]
        var_data = prumeruj_po_4(var_data)
        var_data = np.mean(var_data, axis=(2,3))

        data.extend(var_data)

        # časové štítky
        for i in range(var_data.shape[0]):
            time_labels.append(den_datum(datum_den(f"01/09/{rok}") + z + i, rok))
        z += var_data.shape[0]

    return np.array(data), time_labels, pressure_levels


def wtf():
    folder = f"./Jawara/j{rok}"
    files = sorted([f for f in os.listdir(folder) if f.startswith("T") and f.endswith(".nc")])
    data, time_labels = [], []
    z = 0

    tlak_max = 103.0
    tlak_min = 0.3

    for f in files:
        dataset = Dataset(os.path.join(folder, f))

        # vyber šířky
        sirky = dataset.variables['latitude'][:] if 'latitude' in dataset.variables else dataset.variables['lat'][:]
        lat_idx = np.where((sirky >= 60) & (sirky <= 90))[0]

        # vyber hladin podle tlaku
        all_pressures = dataset.variables['level'][:].astype(float)
        level_idx = np.where((all_pressures <= tlak_max) & (all_pressures >= tlak_min))[0]
        pressure_levels = all_pressures[level_idx]

        # vybraná data a průměr přes lat/lon
        var_data = dataset.variables['t'][:, level_idx, lat_idx, :]
        var_data = prumeruj_po_4(var_data)
        var_data = np.mean(var_data, axis=(2,3))

        data.extend(var_data)

        # časové štítky
        for i in range(var_data.shape[0]):
            time_labels.append(den_datum(datum_den(f"01/09/{rok}") + z + i, rok))
        z += var_data.shape[0]

    return np.array(data), time_labels, pressure_levels

# --- Export rozdílů ---
def lists_to_diff_list(l1, l2, x, y, f):
    with open(f, "w") as o:
        o.write("Date, level, difference value\r\n")
        for i in range(len(x)):
            for j in range(len(y)):
                o.write(f"{x[i]}, {y[j]}, {l1[i][j] - l2[i][j]}\r\n")

def jawara_lat_mean(varname, level, lat_list):

    folder = f"./Jawara/j{rok}"

    if varname == "u":
        files = sorted([f for f in os.listdir(folder) if f.startswith("U") and f.endswith(".nc")])
    elif varname == "t":
        files = sorted([f for f in os.listdir(folder) if f.startswith("T") and f.endswith(".nc")])

    data = []
    time_labels = []
    z = 0

    for f in files:
        dataset = Dataset(os.path.join(folder, f))

        lats = dataset.variables["latitude"][:]
        levs = dataset.variables["level"][:]

        lat_indices = [np.argmin(np.abs(lats - lat)) for lat in lat_list]
        lev_index = np.argmin(np.abs(levs - level))

        var_data = dataset.variables[varname][:, lev_index, lat_indices, :]

        # průměr přes longitude
        var_data = np.mean(var_data, axis=2)

        # průměr po 4 časových krocích (6h → 1 den)
        var_data = prumeruj_po_4(var_data)

        data.extend(var_data)

        # časové popisky (po dnech)
        for i in range(var_data.shape[0]):
            time_labels.append(
                den_datum(datum_den(f"01/12/{rok}") + z + i, rok)
            )

        z += var_data.shape[0]

    return np.array(data), time_labels, lats[lat_indices]