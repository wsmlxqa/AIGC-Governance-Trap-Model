%% ================ Figure 8: Equilibrium Regions in (f_p, u_2) Parameter Space ================
% This script reproduces Figure 8 using only the provided raw data file.
% Required file: figure8.csv

clear; clc; close all;

%% ================== Load Raw Data ==================
data = readtable('figure8.csv');

% Extract unique values and reshape equilibrium map
fp_values   = unique(data.fp);
u2_values   = unique(data.u2);
equilibrium_map = reshape(data.equilibrium_type, length(u2_values), length(fp_values));

fprintf('Data loaded successfully: %d × %d grid (u2 × f_p)\n', length(u2_values), length(fp_values));

%% ================== Create High-Quality Plot ==================
figure('Position', [100 100 850 680], 'Color', 'white');

% Heatmap
imagesc(fp_values, u2_values, equilibrium_map);

% Colormap: Red (Trap) - Yellow (Transitional) - Green (Ideal)
colormap([0.85 0.15 0.15; ...   % User-led Trap (E2)
          0.98 0.75 0.15; ...   % Transitional Region
          0.15 0.70 0.25]);     % Ideal Governance State (E7)

% Colorbar
c = colorbar('Ticks', [1 2 3], ...
    'TickLabels', {'User-led Trap (E_2)', 'Transitional Region', 'Ideal Governance State (E_7)'}, ...
    'FontSize', 12, 'FontName', 'Times New Roman');
c.Label.String = 'Equilibrium Type';
c.Label.FontSize = 13;
c.Label.FontWeight = 'bold';

% Critical threshold: f_p = C_p2 = 80
hold on;
plot([80 80], [min(u2_values) max(u2_values)], '--w', 'LineWidth', 2.8);

% Annotation
text(83, 0.95, 'f_p = C_{p2} = 80', 'Color', 'white', ...
     'FontSize', 12.5, 'FontWeight', 'bold', 'FontName', 'Times New Roman');

% Labels and Title
xlabel('Government Penalty f_p', 'FontSize', 15, 'FontWeight', 'bold', 'FontName', 'Times New Roman');
ylabel('In-stream Moderation Efficiency u_2', 'FontSize', 15, 'FontWeight', 'bold', 'FontName', 'Times New Roman');
title('Equilibrium Regions in (f_p, u_2) Parameter Space', ...
      'FontSize', 16.5, 'FontWeight', 'bold', 'FontName', 'Times New Roman');

% Axis formatting
set(gca, 'YDir', 'normal', ...
         'FontName', 'Times New Roman', ...
         'FontSize', 12, ...
         'LineWidth', 1.1, ...
         'TickDir', 'in', ...
         'Box', 'on');

grid on;

%% ================== Save Publication-Ready Files ==================
print('Figure8', '-dpdf', '-r400');   % Vector format for publication
print('Figure8', '-dpng', '-r400');   % High-resolution raster

fprintf('\n✅ Figure 8 has been successfully generated from figure8.csv\n');
fprintf('   • Output: Figure8.pdf\n');
fprintf('   • Output: Figure8.png\n');