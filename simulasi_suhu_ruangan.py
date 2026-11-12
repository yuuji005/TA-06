"""
TA-06 Pemodelan dan Simulasi - Dynamic System Modelling
Studi kasus: Dinamika suhu ruangan ber-AC (model ODE orde satu)

    C dT/dt = UA (T_amb - T) - Q_c * u/100
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------- Parameter ----------------
C     = 2.0e5     # kapasitas panas ruangan   (J/K)
UA    = 40.0      # konduktansi termal        (W/K)
Q_c   = 600.0     # daya AC pada u = 100%     (W)
T_amb = 32.0      # suhu luar (gangguan)      (°C)
T0    = 32.0      # suhu awal ruangan         (°C)
dt    = 60.0      # langkah waktu             (s)
t_end = 6 * 3600  # lama simulasi 6 jam       (s)

tau = C / UA      # konstanta waktu (s)
t = np.arange(0, t_end + dt, dt)
menit = t / 60.0


def simulasi(u_fungsi, T_amb=T_amb, T0=T0):
    """Euler eksplisit: T[k+1] = T[k] + dt * dT/dt"""
    T = np.zeros_like(t)
    u = np.array([u_fungsi(tk) for tk in t])
    T[0] = T0
    for k in range(len(t) - 1):
        dTdt = (UA * (T_amb - T[k]) - Q_c * u[k] / 100.0) / C
        T[k + 1] = T[k] + dTdt * dt
    return T, u


def T_steady(u_persen):
    return T_amb - Q_c * u_persen / 100.0 / UA


def plot_T(judul, nama_file, label_series):
    """label_series: list (label, T, gaya)"""
    fig, ax = plt.subplots(figsize=(7, 4))
    for lab, T, gaya in label_series:
        ax.plot(menit, T, gaya, label=lab)
    ax.set_xlabel("Waktu (menit)")
    ax.set_ylabel("Suhu ruangan T (°C)")
    ax.set_title(judul)
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(nama_file, dpi=200)
    plt.close(fig)


# ---------------- Sinyal kontrol u(t) (%) ----------------
def u_nol(tk):                  # AC mati
    return 0.0

def u_step(tk):                 # AC 60% mulai t = 30 menit
    return 60.0 if tk >= 30 * 60 else 0.0

def u_pulse(tk):                # AC 60% pada 30-180 menit
    return 60.0 if 30 * 60 <= tk < 180 * 60 else 0.0

def u_ramp(tk):                 # naik 0 -> 100% dalam 3 jam
    return min(100.0, 100.0 * tk / (3 * 3600))

def u_impulse(tk):              # pulsa 100% selama 5 menit
    return 100.0 if 30 * 60 <= tk < 35 * 60 else 0.0

def u_sinus(tk):                # 50% +- 30%, periode 2 jam
    return 50.0 + 30.0 * np.sin(2 * np.pi * tk / (2 * 3600))

def T_analitik_step(tk, u_persen=60.0, t_on=30 * 60):
    Tss = T_steady(u_persen)
    return np.where(tk < t_on, T0,
                    Tss + (T0 - Tss) * np.exp(-(tk - t_on) / tau))


# ---------------- 1. Steady state ----------------
T_a, _ = simulasi(u_nol)
T_b, _ = simulasi(lambda tk: 60.0, T0=T_amb)    # u = 60% sejak awal
print(f"tau = {tau:.0f} s = {tau/60:.1f} menit")
for up in (0, 60, 100):
    print(f"T_ss (u={up}%) = {T_steady(up):.2f} °C")

plot_T("Simulasi Steady State Suhu Ruangan", "grafik_steady_state.png",
       [("u = 0% (AC mati)", T_a, "r-"),
        ("u = 60% sejak t = 0", T_b, "b-"),
        (f"T_ss = {T_steady(60):.1f} °C", np.full_like(t, T_steady(60)), "--")])

# ---------------- 2. Input step (pulsa AC) + validasi analitik ----------------
T_s, u_s = simulasi(u_step)
T_p, u_p = simulasi(u_pulse)
T_an = T_analitik_step(t)
print(f"Galat maks Euler vs analitik = {np.max(np.abs(T_s - T_an)):.4f} °C")

fig, (a1, a2) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
a1.plot(menit, T_p, color="blue")
a1.axhline(T_steady(60), ls=":", color="gray")
a1.set_ylabel("Suhu ruangan T(t) (°C)")
a1.grid(True)
a2.plot(menit, u_p, "--", color="red")
a2.set_ylabel("Kontrol AC u(t) (%)")
a2.set_xlabel("t (menit)")
a2.grid(True)
fig.suptitle("Respon Suhu terhadap Sinyal Step (AC ON 30-180 menit)")
fig.tight_layout()
fig.savefig("grafik_step.png", dpi=200)
plt.close(fig)

plot_T("Validasi Euler vs Solusi Analitik (step 60%)", "grafik_validasi.png",
       [("Euler (dt = 60 s)", T_s, "b-"), ("Analitik", T_an, "--")])

# ---------------- 3. Ramp, impulse, sinusoida ----------------
sinyal = [("Ramp", u_ramp), ("Impulse (pulsa 5 menit)", u_impulse),
          ("Sinusoida", u_sinus)]
fig, axs = plt.subplots(2, 3, figsize=(12, 5.5), sharex=True)
for j, (nama, f) in enumerate(sinyal):
    T_x, u_x = simulasi(f)
    axs[0, j].plot(menit, T_x, color="blue")
    axs[0, j].set_title(nama)
    axs[0, j].grid(True)
    axs[1, j].plot(menit, u_x, "--", color="red")
    axs[1, j].grid(True)
    axs[1, j].set_xlabel("t (menit)")
    print(f"{nama}: T_min = {T_x.min():.2f} C, T_akhir = {T_x[-1]:.2f} °C")
axs[0, 0].set_ylabel("T(t) (°C)")
axs[1, 0].set_ylabel("u(t) (%)")
fig.tight_layout()
fig.savefig("grafik_ramp_impulse_sinus.png", dpi=200)
plt.close(fig)

# ---------------- 4. Gangguan T_amb (sensitivitas) ----------------
seri = []
for Ta in (30.0, 32.0, 34.0):
    T_x, _ = simulasi(lambda tk: 60.0, T_amb=Ta, T0=Ta)
    seri.append((f"T_amb = {Ta:.0f} °C", T_x, "-"))
plot_T("Pengaruh Gangguan Suhu Luar (u = 60%)", "grafik_gangguan.png", seri)

# ---------------- 5. Tabel manual (dt = 600 s) ----------------
print("\nEuler manual, dt = 600 s, u = 60%:")
Tm = 32.0
for k in range(6):
    dTdt = (UA * (T_amb - Tm) - Q_c * 0.6) / C
    Tn = Tm + dTdt * 600
    print(f"t={600*k:5d}s  T={Tm:.4f}  dT/dt={dTdt*1e3:8.4f}e-3  T_next={Tn:.4f}")
    Tm = Tn
