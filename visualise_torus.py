"""
torus32_viz.py
==============

Visualise the "Torus32" number representation (as used e.g. in TFHE-style
homomorphic encryption) as a clock-like diagram.

Idea
----
A torus element is a real number modulo 1, usually kept in the range
[-0.5, 0.5) (equivalently [0, 1)). We draw it as a circle:

    * 0 sits at 12 o'clock.
    * Going CLOCKWISE increases the value: 0 -> 1/q -> 2/q -> ... -> (q-1)/q,
      wrapping back to 0 (=1) at the top again.
    * -0.5 and +0.5 land on the exact same point (6 o'clock) since they are
      equal modulo 1 -- this is the defining feature of the torus.

Two views are provided:

1. plot_torus_wheel(...)   -- reproduces the "roulette wheel" style figure
   (outer ring numbered 0..q-1, quadrant dividers 0/1/2/3, optional shaded
   plaintext slots + a sample noisy point being decoded to its nearest
   plaintext). This mirrors the textbook figure of T_q = {0, 1/q, ..., (q-1)/q}.

2. plot_signed_clock(...)  -- reproduces the hand-drawn sketch: a simple
   clock face labelled with small signed values (-2,-1,0,1,2,...) near the
   top and the wrap-around point (+/- 2^(bits-1)) at the bottom, i.e. the
   32-bit signed integer encoding of a torus element
   (Torus32 stores mu in [-0.5, 0.5) as a signed int32 = round(mu * 2^32)).

Both functions save a PNG and return its path.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _angle_of(frac):
    """Map a torus fraction in [0, 1) to an angle (radians), 0 at 12 o'clock,
    increasing clockwise."""
    return np.pi / 2 - 2 * np.pi * frac


def _circ_dist(a, b):
    """Distance between two points on the torus [0, 1)."""
    d = abs(a - b) % 1.0
    return min(d, 1 - d)


def to_int32(mu, bits=32):
    """Encode a real torus value mu in [-0.5, 0.5) as a signed integer,
    the way TFHE's Torus32 does: round(mu * 2^bits), wrapped to
    [-2^(bits-1), 2^(bits-1) - 1]."""
    modulus = 1 << bits
    raw = int(round(mu * modulus)) % modulus
    half = modulus // 2
    return raw - modulus if raw >= half else raw


# ---------------------------------------------------------------------------
# 1. "roulette wheel" style diagram (like the textbook Example 6 figure)
# ---------------------------------------------------------------------------

def plot_torus_wheel(q=64, p=None, highlight_indices=None, point_value=None,
                      title=None, filename="torus_wheel.png"):
    """
    Draw the discretized torus T_q = {0, 1/q, ..., (q-1)/q} as a numbered
    wheel, optionally highlighting the p plaintext slots and a noisy sample
    point mu* together with its decoded nearest plaintext.

    Parameters
    ----------
    q : int                 number of positions around the wheel (e.g. 64)
    p : int, optional       number of plaintext slots; every q/p-th tick is
                            highlighted (must divide q)
    highlight_indices : list[int], optional
                            explicit indices to highlight instead of using p
    point_value : float, optional
                            a sample value in [-0.5, 0.5) (or [0,1)) to plot
                            as a noisy encoding mu*, with an arrow to the
                            nearest highlighted plaintext
    title : str
    filename : str
    """
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"aspect": "equal"})
    ax.axis("off")

    R_outer, R_inner, R_label = 1.0, 0.75, 1.14

    # outer ring: q numbered wedges
    for i in range(q):
        th1 = np.degrees(_angle_of((i + 1) / q))
        th2 = np.degrees(_angle_of(i / q))
        ax.add_patch(patches.Wedge((0, 0), R_outer, th1, th2,
                                    width=R_outer - R_inner,
                                    facecolor="white", edgecolor="black", lw=0.4))
        mid = _angle_of((i + 0.5) / q)
        lx, ly = (R_outer + R_inner) / 2 * np.cos(mid), (R_outer + R_inner) / 2 * np.sin(mid)
        ax.text(lx, ly, str(i), ha="center", va="center", fontsize=6)

    # figure out which indices are "plaintext" slots
    if highlight_indices is None and p is not None:
        step = q // p
        highlight_indices = [i * step for i in range(p)]

    if highlight_indices:
        for idx in highlight_indices:
            th1 = np.degrees(_angle_of((idx + 1) / q))
            th2 = np.degrees(_angle_of(idx / q))
            ax.add_patch(patches.Wedge((0, 0), R_outer, th1, th2,
                                        width=R_outer - R_inner,
                                        facecolor="black", edgecolor="black"))

    # inner disk
    ax.add_patch(plt.Circle((0, 0), R_inner, facecolor="lightgray",
                             edgecolor="black", lw=1.5))

    # quadrant dividers labelled 0,1,2,3 (as in the textbook figure)
    for k, lbl in enumerate(["0", "1", "2", "3"]):
        a = _angle_of(k / 4)
        x0, y0 = R_inner * np.cos(a), R_inner * np.sin(a)
        x1, y1 = R_outer * np.cos(a), R_outer * np.sin(a)
        ax.plot([x0, x1], [y0, y1], color="black", lw=1)
        lx, ly = R_label * np.cos(a), R_label * np.sin(a)
        ax.text(lx, ly, lbl, ha="center", va="center", fontsize=15, fontweight="bold")

    # center caption
    if p is not None:
        ax.text(0, 0, f"p={p} / q={q}", ha="center", va="center", fontsize=13)

    # sample noisy point + decoding arrow
    if point_value is not None:
        frac = point_value % 1.0
        a = _angle_of(frac)
        px, py = 0.55 * np.cos(a), 0.55 * np.sin(a)
        ax.plot(px, py, "ro", markersize=9, zorder=5)
        ax.annotate(f"$\\mu^*={point_value:.4f}$", (px, py),
                    textcoords="offset points", xytext=(12, 10),
                    color="red", fontsize=11)

        if highlight_indices:
            idx_fracs = [i / q for i in highlight_indices]
            nearest = min(idx_fracs, key=lambda f: _circ_dist(f, frac))
            an = _angle_of(nearest)
            nx, ny = 0.3 * np.cos(an), 0.3 * np.sin(an)
            ax.annotate("", xy=(nx, ny), xytext=(px, py),
                        arrowprops=dict(arrowstyle="->", color="blue", lw=2))
            ax.text(0, -1.25, f"decoded plaintext $\\mu = {nearest:.4f}$",
                    ha="center", fontsize=12, color="blue")

    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    if title:
        ax.set_title(title, fontsize=13)
    plt.tight_layout()
    # plt.savefig(filename, dpi=150)
    plt.show()
    plt.close(fig)
    return filename


# ---------------------------------------------------------------------------
# 2. simple signed "clock face" (like the hand-drawn sketch)
# ---------------------------------------------------------------------------

def plot_signed_clock(bits=32, n_small_ticks=5, point_values=None, point_value=None,
                      title="Torus32 as a signed-integer clock",
                      filename="torus_signed_clock.png"):
    """
    Draw one or more signed-integer torus clocks.

    point_values can be:
        * a single unsigned integer in the range 0 .. 2**bits - 1, or
        * a list/tuple/array of such integers.

    Each supplied value is drawn on its own subplot. Its position is
    point_value / 2**bits around the torus.
    """
    # Backward compatibility: point_value=<int> still works.
    if point_value is not None:
        if point_values is not None:
            raise ValueError("use either point_values or point_value, not both")
        point_values = point_value

    if point_values is None:
        point_values = [None]
    elif isinstance(point_values, (int, np.integer)):
        point_values = [point_values]
    else:
        point_values = list(point_values)
        if len(point_values) == 0:
            raise ValueError("point_values must contain at least one value")

    modulus = 1 << bits
    for value in point_values:
        if value is None:
            continue
        if not isinstance(value, (int, np.integer)):
            raise TypeError("each point_value must be an integer")
        if not 0 <= value < modulus:
            raise ValueError(f"each point_value must be between 0 and {modulus - 1}")

    n = len(point_values)
    ncols = min(n, 3)
    nrows = int(np.ceil(n / ncols))

    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(6 * ncols, 6 * nrows),
        subplot_kw={"aspect": "equal"},
        squeeze=False,
    )
    axes = axes.ravel()

    R = 1.0
    half = 1 << (bits - 1)
    step_deg = 6
    bottom = -np.pi / 2

    for ax, point_value in zip(axes, point_values):
        ax.axis("off")

        circle = plt.Circle((0, 0), R, facecolor="white",
                            edgecolor="crimson", lw=2.5)
        ax.add_patch(circle)

        # Schematic small ticks near the top.
        for k in range(-n_small_ticks, n_small_ticks + 1):
            a = np.pi / 2 - np.radians(k * step_deg)
            x, y = R * np.cos(a), R * np.sin(a)
            tx, ty = 1.13 * np.cos(a), 1.13 * np.sin(a)
            ax.plot([0.93 * np.cos(a), x],
                    [0.93 * np.sin(a), y],
                    color="crimson", lw=1)
            ax.text(tx, ty, str(k), ha="center", va="center",
                    fontsize=11, color="crimson")

        # Wrap-around labels near the bottom.
        for _, lbl, side in [
            (-half, f"$-2^{{{bits-1}}}$", -1),
            (half - 1, f"$2^{{{bits-1}}}-1$", +1),
        ]:
            a = bottom + side * np.radians(step_deg)
            x, y = R * np.cos(a), R * np.sin(a)
            tx, ty = 1.22 * np.cos(a), 1.28 * np.sin(a)
            ax.plot([0.93 * np.cos(a), x],
                    [0.93 * np.sin(a), y],
                    color="crimson", lw=1)
            ax.text(tx, ty, lbl, ha="center", va="center",
                    fontsize=11, color="crimson")

        # Dotted arcs between small ticks and the wrap point.
        for side in (+1, -1):
            a0 = np.pi / 2 - side * np.radians(
                (n_small_ticks + 0.5) * step_deg
            )
            a1 = bottom - side * np.radians(step_deg * 1.5)
            arc_angles = np.linspace(a0, a1, 40)
            ax.plot(np.cos(arc_angles), np.sin(arc_angles),
                    linestyle=(0, (1, 3)), color="crimson", lw=1.2)

        # Vertical divider and sign-bit labels.
        ax.plot([0, 0], [-1.3, 1.3], color="steelblue", lw=3)
        ax.text(-1.5, 0, "0", ha="center", va="center",
                fontsize=20, color="steelblue")
        ax.text(1.5, 0, "1", ha="center", va="center",
                fontsize=20, color="steelblue")

        if point_value is not None:
            frac = point_value / modulus
            a = _angle_of(frac)

            # Radial indicator from centre to slightly outside the clock.
            line_r = 1.08
            px, py = line_r * np.cos(a), line_r * np.sin(a)
            ax.plot([0, px], [0, py], color="darkorange",
                    lw=2.5, zorder=5)

            signed_value = (
                point_value - modulus
                if point_value >= modulus // 2
                else point_value
            )
            ax.annotate(
                f"uint{bits} = {point_value}\nint{bits} = {signed_value}",
                (px, py),
                textcoords="offset points",
                xytext=(10, 8),
                color="darkorange",
                fontsize=10,
            )
            ax.set_title(f"point_value = {point_value}", fontsize=12)

        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)

    # Hide unused subplot slots.
    for ax in axes[n:]:
        ax.axis("off")

    fig.suptitle(title, fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    # plt.savefig(filename, dpi=150)
    plt.show()
    plt.close(fig)
    return filename


# ---------------------------------------------------------------------------
# demo / example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Reproduces the textbook Example 6: p=4 plaintexts, q=64 discretization,
    # with a noisy point mu* = 5/64 that should decode to mu = 0.
    # plot_torus_wheel(q=64, p=4, point_value=5 / 64,
    #                   title="Torus wheel: p=4, q=64 (Example 6 style)",
    #                   filename="/home/michal/torus_wheel_example.png")

    # Simple signed-integer "clock" view for Torus32 (bits=32),
    # with a sample unsigned Torus32 value.
    plot_signed_clock(
        bits=32,
        n_small_ticks=2,
        point_values=[1 << 29, 1 << 30, 3 << 29, 1 << 31, (1 << 32) - 1],
        filename="/home/michal/torus_signed_clock_example.png",
    )

    print("Done. Wrote torus_wheel_example.png and torus_signed_clock_example.png")
