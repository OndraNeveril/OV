import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from zpracovani import *

def vykresli(ax, data, title, xlabels, ylabels, vmin=None, vmax=None, cmap='RdBu_r', p=0, d=False):
    if d:
        cont = ax.contourf(np.array(data).T, cmap=cmap, vmin=(-max(abs(vmin), vmax, 4)), vmax=max(abs(vmin), vmax, 4), levels=100)
    elif p >= 4:
        cont = ax.contourf(np.array(data).T, cmap=cmap, vmin=(-max(abs(vmin), vmax, 70)), vmax=max(abs(vmin), vmax, 70), levels=100)
    else:
        cont = ax.contourf(np.array(data).T, cmap=cmap, vmin=round(int(vmin)/10)*10, vmax=vmax, levels=100)
    if p == 1 or p == 4:
        ax.set_ylabel("Pressure level (hPa)", fontsize=16)
        ax.tick_params(axis='y', labelsize=14)
        ax.set_yticks(range(len(ylabels)))
        ax.set_yticklabels(ylabels)
    else:
        ax.set_yticklabels([])
        ax.set_yticks(range(len(ylabels)))
    if p == 1 or p == 2 or p == 3:
        ax.set_title(title, fontsize=16, weight='bold')
        ax.set_xticks([])
        ax.set_xticklabels([])
    if p == 4 or p == 5 or p == 6:
        if p == 5:
            ax.set_xlabel("Date", fontsize=16)

    xticks = []
    xticklabels = []
    for i, label in enumerate(xlabels):
        day = datetime.strptime(label, "%d/%m/%Y").day
        if day in (1, 15) or i == len(xlabels) - 1:
            xticks.append(i)
            xticklabels.append(format_date_label(label))

    ax.set_xticks(xticks)
    minor_xticks = list(range(len(xlabels) + 1))
    ax.set_xticks(minor_xticks, minor=True)

    if p in (1, 2, 3):
        ax.set_title(title, fontsize=16, weight='bold')
        ax.set_xticklabels([])  # bez textu
        ax.tick_params(axis='x', which='minor', length=3, width=0.7)
        ax.tick_params(axis='x', which='major', length=7, width=1.2)

    if p in (4, 5, 6):
        if p == 5:
            ax.set_xlabel("Date", fontsize=16)
        ax.set_xticklabels(xticklabels, fontsize=14)
        ax.tick_params(axis='x', which='minor', length=3, width=0.7)
        ax.tick_params(axis='x', which='major', length=7, width=1.2)
    if p == 6 and not d:
        sm = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(-70,70), cmap=cmap)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, extend='both', orientation='vertical', fraction=0.046, pad=0.04)
        cbar.set_label("Zonal mean zonal wind (m/s)", labelpad=10, fontsize=16)
        cbar.set_ticks([i for i in range(-70, 80, 20)])
        cbar.ax.tick_params(labelsize=12)
    if p == 3 and d:
        sm = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(-4, 4), cmap=cmap)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, extend='both', orientation='vertical', fraction=0.046, pad=0.04)
        cbar.set_label("Zonal mean temperature (K)", labelpad=10, fontsize=16)
        cbar.set_ticks([i for i in range(-4, 5)])
        cbar.ax.tick_params(labelsize=12)
    if p == 3 and not d:
        sm = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(190, 270), cmap=cmap)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, extend='both', orientation='vertical', fraction=0.046, pad=0.04)
        cbar.set_label("Zonal mean temperature (K)", labelpad=10, fontsize=16)
        cbar.set_ticks([i for i in range(190, 280, 10)])
        cbar.ax.tick_params(labelsize=12)
    if p == 6 and d:
        sm = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(-4, 4), cmap=cmap)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, extend='both', orientation='vertical', fraction=0.046, pad=0.04)
        cbar.set_label("Zonal mean zonal wind (m/s)", labelpad=10, fontsize=16)
        cbar.set_ticks([i for i in range(-4, 5)])
        cbar.ax.tick_params(labelsize=12)
    return cont

eu, ti, p = euf()
et = etf()
mu = muf()
mt = mtf()
ju, _, _ = juf()
jt = jtf()

lists_to_diff_list(eu, mu, ti, p, f"e_vs_m_u_{rok}.csv")
lists_to_diff_list(et, mt, ti, p, f"e_vs_m_t_{rok}.csv")
lists_to_diff_list(mu, ju, ti, p, f"m_vs_j_u_{rok}.csv")
lists_to_diff_list(mt, jt, ti, p, f"m_vs_j_t_{rok}.csv")
lists_to_diff_list(eu, ju, ti, p, f"e_vs_j_u_{rok}.csv")
lists_to_diff_list(et, jt, ti, p, f"e_vs_j_t_{rok}.csv")

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

fig, axs = plt.subplots(2, 3, figsize=(24, 14))
axs = axs.flatten()

tituly = ["ERA5", "MERRA2", "JRA-3Q", "", "", ""]

data_sady = [et_arr, mt_arr, jt, eu_arr, mu_arr, ju]
vmin_sady = [vmin_temp]*3 + [vmin_wind]*3
vmax_sady = [vmax_temp]*3 + [vmax_wind]*3

pp = 0
for ax, title, data, vmin_, vmax_ in zip(axs, tituly, data_sady, vmin_sady, vmax_sady):
    pp += 1
    cbar = vykresli(ax, data, title, ti, p, vmin=vmin_, vmax=vmax_, p=pp)
fig.suptitle(f"SSW Southern hemisphere {rok} winter\n", fontsize=20, weight='bold')

plt.tight_layout()
fig.savefig(f"All_{rok}.png")
plt.close(fig)

fig_all_diff, axs_all = plt.subplots(2, 3, figsize=(24, 14))
axs_all = axs_all.flatten()

tituly_diff_all = ["ERA5 vs. MERRA2", "ERA5 vs. JRA-3Q", "MERRA2 vs. JRA-3Q", "", "", ""]
pp = 0
data_diff_all = [et_mt_diff, et_jt_diff, mt_jt_diff, eu_mu_diff, eu_ju_diff, mu_ju_diff]
vlims_diff = [np.max(np.abs(d)) for d in data_diff_all]

for ax, title, data, vlim in zip(axs_all, tituly_diff_all, data_diff_all, vlims_diff):
    pp += 1
    cbar = vykresli(ax, data, title, ti, p, vmin=-vlim, vmax=vlim, p=pp, d=True)
fig_all_diff.suptitle(f"SSW Southern hemisphere {rok} winter\n", fontsize=20, weight='bold')

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

fig_detail, axs_detail = plt.subplots(2, 3, figsize=(24, 14))
axs_detail = axs_detail.flatten()

tituly_detail = ["ERA5", "MERRA2", "JRA-3Q", "", "", ""]

data_sady_detail = [detail_et, detail_mt, detail_jt, detail_eu, detail_mu, detail_ju]
vmin_sady_detail = [detail_vmin_temp]*3 + [detail_vmin_wind]*3
vmax_sady_detail = [detail_vmax_temp]*3 + [detail_vmax_wind]*3

pp = 0
for ax, title, data, vmin_, vmax_ in zip(axs_detail, tituly_detail, data_sady_detail, vmin_sady_detail, vmax_sady_detail):
    pp += 1
    cbar = vykresli(ax, data, title, ti, detail_p, vmin=vmin_, vmax=vmax_, p=pp)
fig_detail.suptitle(f"SSW Southern hemisphere {rok} winter\n", fontsize=20, weight='bold')

plt.tight_layout()
fig_detail.savefig(f"All_detailed_1_10_{rok}.png")
plt.close(fig_detail)

fig_detail_diff, axs_detail_diff = plt.subplots(2, 3, figsize=(24, 14))
axs_detail_diff = axs_detail_diff.flatten()

tituly_diff_detail = ["ERA5 vs. MERRA2", "ERA5 vs. JRA-3Q", "MERRA2 vs. JRA-3Q", "", "", ""]
# a), ... f)

data_diff_detail = [detail_et_mt_diff, detail_et_jt_diff, detail_mt_jt_diff, detail_eu_mu_diff, detail_eu_ju_diff, detail_mu_ju_diff]
vlims_diff_detail = [np.max(np.abs(d)) for d in data_diff_detail]

pp = 0
for ax, title, data, vlim in zip(axs_detail_diff, tituly_diff_detail, data_diff_detail, vlims_diff_detail):
    pp += 1
    cbar = vykresli(ax, data, title, ti, detail_p, vmin=-vlim, vmax=vlim, p=pp, d=True)
fig_detail_diff.suptitle(f"SSW Southern hemisphere {rok} winter\n", fontsize=20, weight='bold')

plt.tight_layout()
fig_detail_diff.savefig(f"All_differences_detailed_1_10_{rok}.png")
plt.close(fig_detail_diff)