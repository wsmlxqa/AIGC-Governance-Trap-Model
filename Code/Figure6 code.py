import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec

# ==================== Professional Plotting Settings ====================
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 16
rcParams['axes.linewidth'] = 1.5
rcParams['xtick.major.width'] = 1.5
rcParams['ytick.major.width'] = 1.5
rcParams['xtick.major.size'] = 8
rcParams['ytick.major.size'] = 8
rcParams['xtick.minor.size'] = 4
rcParams['ytick.minor.size'] = 4
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'
rcParams['axes.unicode_minus'] = False
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.titleweight'] = 'bold'

# ==================== Load Data ====================
df_A = pd.read_csv('Fig6_Panel_A_Evolution_Data.csv')
df_B = pd.read_csv('Fig6_Panel_B_Velocity_Data.csv')
df_C = pd.read_csv('Fig6_Panel_C_Difference_Data.csv')
df_D = pd.read_csv('Fig6_Panel_D_Cumulative_Data.csv')
df_E = pd.read_csv('Fig6_Panel_E_PhasePortrait_Data.csv')

# Extract data for each panel
t_A = df_A['Time_t']
P_s1 = df_A['Probability_s1_LowIncentive']
P_s2 = df_A['Probability_s2_HighIncentive']
P_s3 = df_A['Probability_s3_HighPenalty']

t_B = df_B['Time_t']
V_s1 = df_B['Velocity_s1_LowIncentive']
V_s2 = df_B['Velocity_s2_HighIncentive']
V_s3 = df_B['Velocity_s3_HighPenalty']

t_C = df_C['Time_t']
diff_s2_s1 = df_C['Difference_HighIncentive_vs_LowIncentive']
diff_s3_s1 = df_C['Difference_HighPenalty_vs_LowIncentive']

t_D = df_D['Time_t']
cum_s1 = df_D['CumulativeChange_s1_LowIncentive']
cum_s2 = df_D['CumulativeChange_s2_HighIncentive']
cum_s3 = df_D['CumulativeChange_s3_HighPenalty']

t_E = df_E['Time_t']
P_s2_phase = df_E['Probability_s2_HighIncentive']
P_s3_phase = df_E['Probability_s3_HighPenalty']

# ==================== Plotting Styles ====================
styles = {
    's1': {'color': '#C44E52', 'marker': 'D', 'ls': '-', 
           'label': r'Low Incentive ($u_2=0.2, f_{b2}=100$)'},
    's2': {'color': '#4C72B0', 'marker': 'o', 'ls': '--', 
           'label': r'High Incentive ($u_2=0.5, f_{b2}=100$)'},
    's3': {'color': '#55A868', 'marker': '^', 'ls': '-.', 
           'label': r'High Penalty ($u_2=0.3, f_{b2}=400$)'}
}

# ==================== Create Figure ====================
fig = plt.figure(figsize=(20, 12), dpi=300, facecolor='white')
gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.3,
              left=0.07, right=0.97, top=0.93, bottom=0.08)

ax1 = fig.add_subplot(gs[0, :2])   # Panel A
ax2 = fig.add_subplot(gs[0, 2])    # Panel B
ax3 = fig.add_subplot(gs[1, 0])    # Panel C
ax4 = fig.add_subplot(gs[1, 1])    # Panel D
ax5 = fig.add_subplot(gs[1, 2])    # Panel E

# --- Panel A: Strategy Evolution ---
step = len(t_A) // 20
ax1.plot(t_A, P_s1, color=styles['s1']['color'], ls=styles['s1']['ls'], lw=3, label=styles['s1']['label'])
ax1.plot(t_A, P_s2, color=styles['s2']['color'], ls=styles['s2']['ls'], lw=3, label=styles['s2']['label'])
ax1.plot(t_A, P_s3, color=styles['s3']['color'], ls=styles['s3']['ls'], lw=3, label=styles['s3']['label'])

ax1.scatter(t_A[::step], P_s1[::step], marker='D', c='none', edgecolors=styles['s1']['color'], s=80, lw=2)
ax1.scatter(t_A[::step], P_s2[::step], marker='o', c='none', edgecolors=styles['s2']['color'], s=80, lw=2)
ax1.scatter(t_A[::step], P_s3[::step], marker='^', c='none', edgecolors=styles['s3']['color'], s=80, lw=2)

ax1.annotate('Initial State\n$P_0 = 0.5$', xy=(0, 0.5), xytext=(0.02, 0.25),
             arrowprops=dict(arrowstyle='->', lw=2, color='#333', connectionstyle="arc3,rad=0.3"),
             fontsize=14, bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.8))
ax1.axvspan(0, 0.03, color='grey', alpha=0.15, label='Decision Window')

ax1.set_xlabel('Evolutionary Time ($t$)')
ax1.set_ylabel('Probability of Compliance ($P$)')
ax1.set_title('A: Creator Strategy Evolution under Different Regulations')
ax1.legend(loc='center right', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.6)

# --- Panel B: Velocity ---
ax2.plot(t_B, V_s1, color=styles['s1']['color'], ls=styles['s1']['ls'], lw=2.5)
ax2.plot(t_B, V_s2, color=styles['s2']['color'], ls=styles['s2']['ls'], lw=2.5)
ax2.plot(t_B, V_s3, color=styles['s3']['color'], ls=styles['s3']['ls'], lw=2.5)
ax2.axhline(0, color='black', lw=1.5, ls=':')
ax2.set_xlabel('Time ($t$)')
ax2.set_ylabel('Evolution Velocity ($dP/dt$)')
ax2.set_title('B: Rate of Strategy Change')
ax2.grid(True, linestyle='--', alpha=0.6)

# --- Panel C: Strategy Difference ---
ax3.plot(t_C, diff_s2_s1, color=styles['s2']['color'], ls=styles['s2']['ls'], lw=2.5, 
         label='High Incentive vs. Low Incentive')
ax3.plot(t_C, diff_s3_s1, color=styles['s3']['color'], ls=styles['s3']['ls'], lw=2.5, 
         label='High Penalty vs. Low Incentive')
ax3.fill_between(t_C, diff_s2_s1, 0, color=styles['s2']['color'], alpha=0.15)
ax3.fill_between(t_C, diff_s3_s1, 0, color=styles['s3']['color'], alpha=0.15)
ax3.set_xlabel('Time ($t$)')
ax3.set_ylabel('Strategy Difference ($\Delta P$)')
ax3.set_title('C: Divergence from Baseline')
ax3.legend(fontsize=11)
ax3.grid(True, linestyle='--', alpha=0.6)

# --- Panel D: Cumulative Change ---
ax4.plot(t_D, cum_s1, color=styles['s1']['color'], ls=styles['s1']['ls'], lw=3, 
         marker='D', markersize=6, markevery=step, label=styles['s1']['label'])
ax4.plot(t_D, cum_s2, color=styles['s2']['color'], ls=styles['s2']['ls'], lw=3, 
         marker='o', markersize=6, markevery=step, label=styles['s2']['label'])
ax4.plot(t_D, cum_s3, color=styles['s3']['color'], ls=styles['s3']['ls'], lw=3, 
         marker='^', markersize=6, markevery=step, label=styles['s3']['label'])
ax4.set_xlabel('Time ($t$)')
ax4.set_ylabel(r'Cumulative Change ($ \int |dP/dt| \, dt $)')
ax4.set_title('D: Total Strategic Shift')
ax4.legend(fontsize=11)
ax4.grid(True, linestyle='--', alpha=0.6)

# --- Panel E: Phase Portrait ---
scatter = ax5.scatter(P_s2_phase, P_s3_phase, c=t_E, cmap='viridis', s=20, zorder=5)
ax5.plot(P_s2_phase, P_s3_phase, color='grey', lw=1, alpha=0.5, zorder=4)
ax5.scatter(P_s2_phase.iloc[0], P_s3_phase.iloc[0], s=200, marker='o', c='red', 
            edgecolors='k', zorder=10, label='Start (t=0)')
ax5.scatter(P_s2_phase.iloc[-1], P_s3_phase.iloc[-1], s=250, marker='*', c='gold', 
            edgecolors='k', zorder=10, label='End (Equilibrium)')

ax5.set_xlabel('High Incentive Prob. ($P_{s2}$)')
ax5.set_ylabel('High Penalty Prob. ($P_{s3}$)')
ax5.set_title('E: Phase Portrait of Effective Strategies')
ax5.legend(fontsize=11)
ax5.grid(True, linestyle='--', alpha=0.6)
cbar = fig.colorbar(scatter, ax=ax5)
cbar.set_label('Time Evolution ($t$)')

# ==================== Overall Formatting ====================
fig.suptitle('Comprehensive Analysis of Regulatory Impact on Creator Compliance Evolution', 
             fontsize=24)

for ax in fig.get_axes():
    ax.tick_params(top=True, right=True, which='both')
    ax.set_xlim(left=-0.005, right=0.205)

ax1.set_ylim(-0.1, 1.1)
ax5.set_xlim(0.45, 1.05)
ax5.set_ylim(0.45, 1.05)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# ==================== Save Figure ====================
plt.savefig("Figure6.pdf", bbox_inches='tight', dpi=300)
plt.savefig("Figure6.png", bbox_inches='tight', dpi=300)
plt.close()