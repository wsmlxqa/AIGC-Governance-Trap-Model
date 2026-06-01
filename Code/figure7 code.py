import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches

# ==================== Configuration ====================
DATA_FILENAME = 'figure_7.csv'

# ==================== Plotting Settings ====================
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'stix'

rcParams['axes.linewidth'] = 1.2
rcParams['xtick.major.width'] = 1.2
rcParams['ytick.major.width'] = 1.2
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'
rcParams['axes.unicode_minus'] = False

# ==================== Load and Prepare Data ====================
df = pd.read_csv(DATA_FILENAME)

t = df['Time (t)'].values
p_baseline = df['P(Ebl=600, u1=0.3, u2=0.3)'].values
p_high_e   = df['P(Ebl=900, u1=0.3, u2=0.3)'].values
p_high_u2  = df['P(Ebl=900, u1=0.3, u2=0.5)'].values
p_high_u1  = df['P(Ebl=900, u1=0.6, u2=0.3)'].values

raw_data = {
    'Baseline': p_baseline,
    'High E_bl': p_high_e,
    'High u2': p_high_u2,
    'High u1': p_high_u1
}

# Smooth interpolation
t_smooth = np.linspace(t.min(), t.max(), 300)
dt = t_smooth[1] - t_smooth[0]
processed_data = {}
for name, p_values in raw_data.items():
    spl = make_interp_spline(t, p_values, k=3)
    p_smooth = np.clip(spl(t_smooth), 0, 1)
    rate = np.gradient(p_smooth, dt)
    processed_data[name] = {'p': p_smooth, 'rate': rate}

# Plotting styles
styles = {
    'Baseline':  {'color': '#696969', 'ls': '--', 
                  'label': r'Baseline: $E_{bl}=600, u_1=0.3, u_2=0.3$'},
    'High E_bl': {'color': '#0072B2', 'ls': '-',  
                  'label': r'High $E_{bl}=900$'},
    'High u2':   {'color': '#D55E00', 'ls': '-',  
                  'label': r'High $u_2=0.5$'},
    'High u1':   {'color': '#009E73', 'ls': '-',  
                  'label': r'High $u_1=0.6$'}
}

# ==================== Create Figure ====================
fig = plt.figure(figsize=(18, 12), dpi=300)
gs = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35,
              left=0.07, right=0.97, top=0.93, bottom=0.07)

# --- Panel (a): Main Evolutionary Dynamics ---
ax1 = fig.add_subplot(gs[0, 0:2])
for name, style in styles.items():
    ax1.plot(t_smooth, processed_data[name]['p'], 
             color=style['color'], lw=2.5, ls=style['ls'], label=style['label'])

ax1.set_title('Main Evolutionary Dynamics', fontsize=16, fontweight='bold', pad=10)
ax1.set_xlabel('Evolutionary Time $t$', fontsize=14)
ax1.set_ylabel('Probability of Creator Compliance', fontsize=14)
ax1.set_xlim(-0.005, 0.205)
ax1.set_ylim(-0.05, 1.05)
ax1.grid(linestyle=':', linewidth=0.5, alpha=0.7)
ax1.legend(loc='lower left', fontsize=11, frameon=True, fancybox=True, edgecolor='black')
ax1.text(-0.1, 1.05, '(a)', transform=ax1.transAxes, fontsize=20, weight='bold')

# --- Panel (b): Evolutionary Rate ---
ax2 = fig.add_subplot(gs[0, 2])
for name, style in styles.items():
    ax2.plot(t_smooth, processed_data[name]['rate'], 
             color=style['color'], lw=2.5, ls=style['ls'])
ax2.axhline(0, color='black', lw=1.2, ls='-')
ax2.set_title('Evolutionary Rate Analysis', fontsize=16, fontweight='bold', pad=10)
ax2.set_xlabel('Evolutionary Time $t$', fontsize=14)
ax2.set_ylabel('Rate of Change $dP/dt$', fontsize=14)
ax2.grid(linestyle=':', linewidth=0.5, alpha=0.7)
ax2.text(-0.2, 1.05, '(b)', transform=ax2.transAxes, fontsize=20, weight='bold')

# --- Panel (c): Impact Magnitude vs. Baseline ---
ax3 = fig.add_subplot(gs[1, 0])
p_baseline_smooth = processed_data['Baseline']['p']
scenarios_to_compare = ['High E_bl', 'High u2', 'High u1']
for name in scenarios_to_compare:
    style = styles[name]
    delta_p = processed_data[name]['p'] - p_baseline_smooth
    ax3.plot(t_smooth, delta_p, color=style['color'], lw=2.5, 
             ls=style['ls'], label=style['label'])
    ax3.fill_between(t_smooth, 0, delta_p, color=style['color'], alpha=0.15)
ax3.axhline(0, color='black', lw=1.2, ls='-')
ax3.set_title('Impact Magnitude vs. Baseline', fontsize=16, fontweight='bold', pad=10)
ax3.set_xlabel('Evolutionary Time $t$', fontsize=14)
ax3.set_ylabel('Change in Probability $\Delta P$', fontsize=14)
ax3.legend(loc='upper right', fontsize=11, frameon=True)
ax3.grid(linestyle=':', linewidth=0.5, alpha=0.7)
ax3.text(-0.2, 1.05, '(c)', transform=ax3.transAxes, fontsize=20, weight='bold')

# --- Panel (d): Convergence to Equilibrium ---
ax4 = fig.add_subplot(gs[1, 1])
equilibria = {'Baseline': 1.0, 'High E_bl': 0.0, 
              'High u2': 1.0, 'High u1': 1.0}
for name, style in styles.items():
    distance = np.abs(processed_data[name]['p'] - equilibria[name])
    ax4.plot(t_smooth, distance, color=style['color'], lw=2.5, ls=style['ls'])
ax4.set_title('Convergence to Equilibrium', fontsize=16, fontweight='bold', pad=10)
ax4.set_xlabel('Evolutionary Time $t$', fontsize=14)
ax4.set_ylabel('Distance to Equilibrium $|P - P^*|$', fontsize=14)
ax4.set_yscale('log')
ax4.set_ylim(bottom=1e-3, top=1.0)
ax4.grid(which='both', linestyle=':', linewidth=0.5, alpha=0.7)
ax4.text(-0.2, 1.05, '(d)', transform=ax4.transAxes, fontsize=20, weight='bold')

# --- Panel (e): Parameter Space Projection ---
ax5 = fig.add_subplot(gs[1, 2])
color_map = {'Compliance': '#009E73', 'Violation': '#0072B2'}
param_points = {
    'Baseline':  {'E_bl': 600, 'u': 0.3, 'p_final': 'Compliance', 'marker': 'o', 'ms': 12},
    'High E_bl': {'E_bl': 900, 'u': 0.3, 'p_final': 'Violation',  'marker': 's', 'ms': 11},
    'High u2':   {'E_bl': 600, 'u': 0.5, 'p_final': 'Compliance', 'marker': '^', 'ms': 12},
    'High u1':   {'E_bl': 600, 'u': 0.6, 'p_final': 'Compliance', 'marker': 'D', 'ms': 11}
}

for name, params in param_points.items():
    ax5.plot(params['E_bl'], params['u'], marker=params['marker'], 
             markersize=params['ms'], color=color_map[params['p_final']], 
             markeredgecolor='black', markeredgewidth=1.2, linestyle='None', label=name)

ax5.set_title('Parameter Space Projection', fontsize=16, fontweight='bold', pad=10)
ax5.set_xlabel('Violation Income ($E_{bl}$)', fontsize=14)
ax5.set_ylabel('Platform Efficiency ($u_1$ or $u_2$)', fontsize=14)
ax5.grid(linestyle=':', linewidth=0.5, alpha=0.7)
ax5.set_xlim(550, 950)
ax5.set_ylim(0.25, 0.65)
ax5.text(-0.2, 1.05, '(e)', transform=ax5.transAxes, fontsize=20, weight='bold')

# Legend for final states
handles, labels = ax5.get_legend_handles_labels()
ax5.legend(handles=handles, labels=labels, loc='upper right',
           title='Scenarios', title_fontsize=13, fontsize=11, 
           fancybox=True, framealpha=0.9)

compliance_patch = mpatches.Patch(color=color_map['Compliance'], label='Compliance ($P^*=1$)')
violation_patch = mpatches.Patch(color=color_map['Violation'], label='Violation ($P^*=0$)')
ax5.legend(handles=[compliance_patch, violation_patch], loc='lower right',
           title='Final State', title_fontsize=13, fontsize=11, 
           fancybox=True, framealpha=0.9)

# ==================== Overall Title and Save ====================
fig.suptitle('Comprehensive Analysis of Creator and Platform Strategy Evolution', 
             fontsize=22, fontweight='bold', y=0.985)

plt.savefig('Figure7.pdf', bbox_inches='tight', format='pdf')
plt.savefig('Figure7.png', bbox_inches='tight', dpi=600)
plt.close()