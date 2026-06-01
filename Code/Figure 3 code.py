import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle

# Load the dataset
df = pd.read_csv('figure3.csv')

# Configure journal plotting standards
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 12,
    'axes.linewidth': 1.5,
    'mathtext.fontset': 'stix'
})

fig = plt.figure(figsize=(16, 9), dpi=300)
gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3, left=0.08, right=0.96, top=0.93, bottom=0.08)

# Color scheme
colors = {'platform': '#DC143C', 'creator': '#1E90FF', 'user': '#228B22'}

# Panel A: Strategy Adoption Dynamics
ax1 = fig.add_subplot(gs[0, :2])
ax1.plot(df['Time_t'], df['Platform_P'], color=colors['platform'], lw=3, label='Platform')
ax1.plot(df['Time_t'], df['Creator_P'], color=colors['creator'], lw=3, label='Creator')
ax1.plot(df['Time_t'], df['User_P'], color=colors['user'], lw=3, label='User')
ax1.set_xlabel('Evolutionary Time $t$', fontweight='bold')
ax1.set_ylabel('Strategy Adoption Probability $P(t)$', fontweight='bold')
ax1.legend(frameon=True)
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.text(-0.05, 1.05, 'A', transform=ax1.transAxes, fontsize=20, fontweight='bold')

# Panel B: Evolution Rate
ax2 = fig.add_subplot(gs[0, 2])
ax2.plot(df['Time_t'], df['Rate_Platform'], color=colors['platform'], lw=2)
ax2.plot(df['Time_t'], df['Rate_Creator'], color=colors['creator'], lw=2)
ax2.plot(df['Time_t'], df['Rate_User'], color=colors['user'], lw=2)
ax2.set_xlabel('Time $t$', fontweight='bold')
ax2.set_ylabel('Evolution Rate $dP/dt$', fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.text(-0.15, 1.05, 'B', transform=ax2.transAxes, fontsize=20, fontweight='bold')

# Panel C: Strategy Difference
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(df['Time_t'], df['Diff_User_Platform'], color='#8B008B', lw=2, label='User - Platform')
ax3.plot(df['Time_t'], df['Diff_Platform_Creator'], color='#FF8C00', lw=2, label='Platform - Creator')
ax3.set_xlabel('Time $t$', fontweight='bold')
ax3.set_ylabel('Strategy Difference $\\Delta P$', fontweight='bold')
ax3.legend(fontsize=9)
ax3.grid(True, linestyle='--', alpha=0.3)
ax3.text(-0.15, 1.05, 'C', transform=ax3.transAxes, fontsize=20, fontweight='bold')

# Panel D: Cumulative Change
ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(df['Time_t'], df['Cum_Change_Platform'], color=colors['platform'], lw=2)
ax4.plot(df['Time_t'], df['Cum_Change_Creator'], color=colors['creator'], lw=2)
ax4.plot(df['Time_t'], df['Cum_Change_User'], color=colors['user'], lw=2)
ax4.set_xlabel('Time $t$', fontweight='bold')
ax4.set_ylabel('Cumulative Change $|\\Delta P|$', fontweight='bold')
ax4.grid(True, linestyle='--', alpha=0.3)
ax4.text(-0.15, 1.05, 'D', transform=ax4.transAxes, fontsize=20, fontweight='bold')

# Panel E: Phase Space
ax5 = fig.add_subplot(gs[1, 2])
sc = ax5.scatter(df['Platform_P'], df['User_P'], c=df['Time_t'], cmap='viridis', s=10)
ax5.set_xlabel('Platform Probability $P_{platform}$', fontweight='bold')
ax5.set_ylabel('User Probability $P_{user}$', fontweight='bold')
cbar = plt.colorbar(sc, ax=ax5)
cbar.set_label('Time $t$')
ax5.grid(True, linestyle='--', alpha=0.3)
ax5.text(-0.15, 1.05, 'E', transform=ax5.transAxes, fontsize=20, fontweight='bold')

plt.tight_layout()
plt.savefig('Figure3.pdf', bbox_inches='tight')
plt.show()