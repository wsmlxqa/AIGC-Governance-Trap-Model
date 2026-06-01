import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.signal import savgol_filter

# ==================== Plotting Style Settings ====================
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "axes.labelsize": 13,
    "axes.titlesize": 15,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 10,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "savefig.dpi": 300,
    "figure.figsize": (18, 10),
    "savefig.bbox": "tight",
    "savefig.facecolor": "white"
})

# Color scheme
colors = {
    'platform': '#DC143C',
    'creator': '#1E90FF',
    'user': '#228B22'
}

# ==================== Load Data ====================
data_df = pd.read_csv('figure5.csv')

t = data_df['time'].values
y_platform = data_df['platform_strategy'].values
y_creator = data_df['creator_strategy'].values
y_user = data_df['user_strategy'].values

# Light smoothing to reduce noise
window_size = 51
poly_order = 3
y_platform = savgol_filter(y_platform, window_length=window_size, polyorder=poly_order)
y_creator = savgol_filter(y_creator, window_length=window_size, polyorder=poly_order)
y_user = savgol_filter(y_user, window_length=window_size, polyorder=poly_order)

# ==================== Create Figure ====================
fig = plt.figure(figsize=(18, 10), dpi=300)
gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35,
              left=0.08, right=0.96, top=0.93, bottom=0.08)

# ==================== Panel A: Evolution Dynamics ====================
ax1 = fig.add_subplot(gs[0, :2])
ax1.plot(t, y_platform, linewidth=2.2, color=colors['platform'], label='Platform')
ax1.plot(t, y_creator, linewidth=2.2, color=colors['creator'], label='Creator')
ax1.plot(t, y_user, linewidth=2.2, color=colors['user'], label='User')

low_valley = (y_platform < 0.3) & (y_creator < 0.3)
ax1.fill_between(t, 0, 1, where=low_valley, color='gray', alpha=0.15, label='Dual Low Period')

ax1.set_xlabel('Time $t$')
ax1.set_ylabel('Strategy Selection Probability')
ax1.set_title('Evolution Dynamics Among Three Entities (Creator Phase Lag)', pad=15)
ax1.set_xlim(t.min(), t.max())
ax1.set_ylim(-0.05, 1.05)
ax1.legend(loc='lower right', frameon=True, fancybox=True, fontsize=12)
ax1.text(-0.08, 1.08, 'A', transform=ax1.transAxes, fontsize=20, weight='bold', va='top', ha='left')

# ==================== Panel B: Evolution Rate ====================
ax2 = fig.add_subplot(gs[0, 2])
dt = t[1] - t[0]
rate_platform = np.gradient(y_platform, dt)
rate_creator = np.gradient(y_creator, dt)
rate_user = np.gradient(y_user, dt)

ax2.plot(t, rate_platform, linewidth=2, color=colors['platform'], label='Platform')
ax2.plot(t, rate_creator, linewidth=2, color=colors['creator'], label='Creator')
ax2.plot(t, rate_user, linewidth=2, color=colors['user'], label='User')
ax2.axhline(y=0, color='black', linewidth=1.5, linestyle='--', alpha=0.5)
ax2.fill_between(t, 0, rate_platform, alpha=0.2, color=colors['platform'])
ax2.fill_between(t, 0, rate_creator, alpha=0.2, color=colors['creator'])
ax2.fill_between(t, 0, rate_user, alpha=0.2, color=colors['user'])

ax2.set_xlabel('Time $t$')
ax2.set_ylabel(r'Evolution Rate $dP/dt$')
ax2.set_title('Analysis of Evolution Rate', pad=15)
ax2.set_xlim(t.min(), t.max())
ax2.legend(fontsize=10, loc='upper right')
ax2.text(-0.15, 1.08, 'B', transform=ax2.transAxes, fontsize=20, weight='bold', va='top', ha='left')

# ==================== Panel C: Relative Strategy Differences ====================
ax3 = fig.add_subplot(gs[1, 0])
diff_pc = y_platform - y_creator
diff_pu = y_platform - y_user
diff_cu = y_creator - y_user

ax3.plot(t, diff_pc, linewidth=2, color='#FF8C00', label='Platform-Creator')
ax3.plot(t, diff_pu, linewidth=2, color='#8B008B', label='Platform-User')
ax3.plot(t, diff_cu, linewidth=2, color='#7CFC00', label='Creator-User')
ax3.axhline(y=0, color='black', linewidth=1.5, linestyle='--', alpha=0.5)
ax3.fill_between(t, 0, diff_pc, alpha=0.15, color='#FF8C00')
ax3.fill_between(t, 0, diff_pu, alpha=0.15, color='#8B008B')
ax3.fill_between(t, 0, diff_cu, alpha=0.15, color='#7CFC00')

ax3.set_xlabel('Time $t$')
ax3.set_ylabel(r'Strategy Difference $\Delta P$')
ax3.set_title('Relative Strategy Differences', pad=15)
ax3.set_xlim(t.min(), t.max())
ax3.legend(fontsize=9, loc='upper right')
ax3.text(-0.15, 1.08, 'C', transform=ax3.transAxes, fontsize=20, weight='bold', va='top', ha='left')

# ==================== Panel D: Cumulative Changes ====================
ax4 = fig.add_subplot(gs[1, 1])
cumulative_platform = np.abs(y_platform - y_platform[0])
cumulative_creator = np.abs(y_creator - y_creator[0])
cumulative_user = np.abs(y_user - y_user[0])

ax4.plot(t, cumulative_platform, linewidth=2, color=colors['platform'], label='Platform')
ax4.plot(t, cumulative_creator, linewidth=2, color=colors['creator'], label='Creator')
ax4.plot(t, cumulative_user, linewidth=2, color=colors['user'], label='User')
ax4.fill_between(t, 0, cumulative_platform, alpha=0.15, color=colors['platform'])
ax4.fill_between(t, 0, cumulative_creator, alpha=0.15, color=colors['creator'])
ax4.fill_between(t, 0, cumulative_user, alpha=0.15, color=colors['user'])

ax4.set_xlabel('Time $t$')
ax4.set_ylabel(r'Cumulative Change $|\Delta P|$')
ax4.set_title('Cumulative Changes', pad=15)
ax4.set_xlim(t.min(), t.max())
ax4.legend(fontsize=10, loc='lower right')
ax4.text(-0.15, 1.08, 'D', transform=ax4.transAxes, fontsize=20, weight='bold', va='top', ha='left')

# ==================== Panel E: Phase Diagram ====================
ax5 = fig.add_subplot(gs[1, 2])
scatter = ax5.scatter(y_platform, y_user, c=t, cmap='viridis', s=15, alpha=0.8, edgecolors='none')

# Evolution direction arrows
arrow_indices = np.linspace(0, len(t)-1, 8, dtype=int)[:-1]
for idx in arrow_indices:
    next_idx = idx + 50 if idx + 50 < len(t) else -1
    ax5.annotate('', xy=(y_platform[next_idx], y_user[next_idx]),
                 xytext=(y_platform[idx], y_user[idx]),
                 arrowprops=dict(arrowstyle='->', lw=2, color='red', alpha=0.7))

ax5.scatter(y_platform[0], y_user[0], s=300, marker='o', color='red', edgecolors='white',
            linewidth=3, zorder=10, label='Start Point')
ax5.scatter(y_platform[-1], y_user[-1], s=300, marker='*', color='gold', edgecolors='black',
            linewidth=2, zorder=10, label='End Point')

ax5.set_xlabel(r'Platform Probability $P_{\mathrm{platform}}$')
ax5.set_ylabel(r'User Probability $P_{\mathrm{user}}$')
ax5.set_title('Strategy Space Phase Diagram (Platform vs User)', pad=15)
ax5.set_xlim(-0.05, 1.05)
ax5.set_ylim(0.85, 1.05)
ax5.legend(fontsize=10, loc='lower right')
cbar = plt.colorbar(scatter, ax=ax5, pad=0.02)
cbar.set_label('Time $t$', fontsize=12, fontweight='bold')
ax5.text(-0.15, 1.08, 'E', transform=ax5.transAxes, fontsize=20, weight='bold', va='top', ha='left')

# ==================== Save Figure ====================
plt.savefig('Figure5.pdf', format='pdf')
plt.savefig('Figure5.png', format='png', dpi=300)
plt.savefig('Figure5.tiff', format='tiff', pil_kwargs={"compression": "tiff_lzw"})

plt.close()