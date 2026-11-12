import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, FancyArrowPatch, Polygon, Circle

fig, ax = plt.subplots(figsize=(9, 4.6))
ax.set_xlim(0, 18); ax.set_ylim(-0.4, 9.2); ax.axis("off")

def cloud(x, y):
    ax.add_patch(Ellipse((x, y), 1.8, 1.2, fc="#e8e8e8", ec="#666", lw=1.5))

def valve(x, y):
    ax.add_patch(Polygon([[x-.35, y+.35], [x-.35, y-.35], [x+.35, y+.35], [x+.35, y-.35]],
                         closed=True, fc="white", ec="black", lw=1.5, zorder=5))

def arrow(p, q, **kw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, lw=2, color=kw.get("c", "#1f4e9c"), zorder=2,
                                 connectionstyle=kw.get("cs", "arc3")))

def aux(x, y, txt, fc="#fff2cc"):
    ax.add_patch(Circle((x, y), .95, fc=fc, ec="#b8860b", lw=1.3, zorder=4))
    ax.text(x, y, txt, ha="center", va="center", fontsize=9, zorder=5)

# stock
ax.add_patch(Rectangle((7, 3.1), 4, 2.4, fc="#cfe2f3", ec="#1f4e9c", lw=2.5, zorder=3))
ax.text(9, 4.65, "STOCK", ha="center", fontsize=9, color="#1f4e9c", weight="bold")
ax.text(9, 4.0, "Energi panas ruangan", ha="center", fontsize=10)
ax.text(9, 3.4, r"$E = C\,T$  →  suhu $T$ (°C)", ha="center", fontsize=10)

# clouds & flows
cloud(1.3, 4.3); cloud(16.7, 4.3)
arrow((2.2, 4.3), (7, 4.3)); arrow((11, 4.3), (15.8, 4.3))
valve(4.6, 4.3); valve(13.4, 4.3)
ax.text(4.6, 3.55, "FLOW masuk\n" r"$Q_{in}=UA\,(T_{amb}-T)$", ha="center", va="top", fontsize=9.5)
ax.text(13.4, 3.55, "FLOW keluar\n" r"$Q_{AC}=Q_c\,u/100$", ha="center", va="top", fontsize=9.5)
ax.text(1.3, 3.45, "panas dari luar", ha="center", va="top", fontsize=8.5)
ax.text(16.7, 3.45, "panas dibuang AC", ha="center", va="top", fontsize=8.5)

# auxiliaries (input)
aux(4.6, 7.9, r"$T_{amb}$" "\n(gangguan)")
aux(13.4, 7.9, r"$u$" "\n(kontrol)")
arrow((4.6, 6.95), (4.6, 4.75), c="#b8860b"); arrow((13.4, 6.95), (13.4, 4.75), c="#b8860b")

# feedback
arrow((8.2, 5.5), (5.05, 4.7), c="#c0392b", cs="arc3,rad=0.3")
ax.text(8.6, 7.0, "umpan balik negatif (balancing):\n$T$ naik → $Q_{in}$ turun", ha="center", fontsize=9, color="#c0392b")

# parameter & output
ax.text(9, 1.55, "Parameter konstan:  $C$ = kapasitas panas,  $UA$ = konduktansi termal,  $Q_c$ = daya pendingin maks.",
        ha="center", fontsize=9.5, bbox=dict(boxstyle="round", fc="#fff2cc", ec="#b8860b"))
ax.text(9, 0.35, r"$C\,\dfrac{dT}{dt}=UA\,(T_{amb}-T)-Q_c\,\dfrac{u}{100}$", ha="center", fontsize=12)
ax.text(9, 5.75, "output: $T(t)$", ha="center", fontsize=9.5, color="#1f4e9c", weight="bold")
fig.savefig("diagram_stock_flow.png", dpi=200, bbox_inches="tight", facecolor="white")
