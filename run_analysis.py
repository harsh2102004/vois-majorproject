import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend so it works without a display
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style='whitegrid', palette='viridis')
plt.rcParams['figure.dpi'] = 120
SEASON_COLORS = {'Kharif': '#2ecc71', 'Rabi': '#3498db', 'Zaid': '#e67e22'}

# ── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv('agriculture_dataset.csv')
print(f'Dataset shape: {df.shape}')
print(df.head(2).to_string())

# ── Cleaning ──────────────────────────────────────────────────────────────────
print('\n=== Missing Values ===')
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else 'No missing values!')
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
print('Data cleaning complete.')
print('Seasons:', df['Season'].value_counts().to_dict())
print('Crops:', df['Crop'].value_counts().to_dict())
print('States:', df['State'].nunique(), 'unique states')

# ── 1. Seasonal Performance ────────────────────────────────────────────────────
seasonal = df.groupby('Season').agg(
    Avg_Yield=('Yield_Tonnes_Ha', 'mean'),
    Avg_Profit=('Profit_INR', 'mean'),
    Avg_Revenue=('Revenue_INR', 'mean'),
    Avg_Cost=('Total_Cost_INR', 'mean'),
    Count=('Farm_ID', 'count')
).reset_index()

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Seasonal Agricultural Performance Overview', fontsize=16, fontweight='bold', y=1.02)

bars = axes[0].bar(seasonal['Season'], seasonal['Avg_Yield'],
                   color=[SEASON_COLORS[s] for s in seasonal['Season']], edgecolor='white', linewidth=1.5)
axes[0].bar_label(bars, fmt='%.2f t/ha', padding=3, fontsize=9)
axes[0].set_title('Average Yield (Tonnes/Ha)', fontweight='bold')
axes[0].set_ylabel('Yield (t/ha)')

bars2 = axes[1].bar(seasonal['Season'], seasonal['Avg_Profit'] / 1e3,
                    color=[SEASON_COLORS[s] for s in seasonal['Season']], edgecolor='white', linewidth=1.5)
axes[1].bar_label(bars2, fmt='%.0f K', padding=3, fontsize=9)
axes[1].set_title('Average Profit (INR)', fontweight='bold')
axes[1].set_ylabel('Profit (Thousands INR)')
axes[1].axhline(0, color='red', linestyle='--', linewidth=0.8, alpha=0.6)

x = np.arange(len(seasonal))
w = 0.35
axes[2].bar(x - w/2, seasonal['Avg_Revenue'] / 1e3, w, label='Revenue', color='#2ecc71', edgecolor='white')
axes[2].bar(x + w/2, seasonal['Avg_Cost'] / 1e3, w, label='Cost', color='#e74c3c', edgecolor='white')
axes[2].set_xticks(x)
axes[2].set_xticklabels(seasonal['Season'])
axes[2].set_title('Revenue vs Cost by Season', fontweight='bold')
axes[2].set_ylabel('Amount (Thousands INR)')
axes[2].legend()

plt.tight_layout()
plt.savefig('seasonal_performance.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: seasonal_performance.png')
print(seasonal.to_string(index=False))

# ── 2. Crop-Season Heatmaps ────────────────────────────────────────────────────
crop_season = df.groupby(['Season', 'Crop']).agg(
    Avg_Yield=('Yield_Tonnes_Ha', 'mean'),
    Avg_Profit=('Profit_INR', 'mean')
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(18, 6))
fig.suptitle('Crop Performance by Season', fontsize=15, fontweight='bold')

pivot_yield = crop_season.pivot(index='Crop', columns='Season', values='Avg_Yield')
sns.heatmap(pivot_yield, annot=True, fmt='.2f', cmap='YlGn', ax=axes[0],
            linewidths=0.5, cbar_kws={'label': 'Avg Yield (t/ha)'})
axes[0].set_title('Average Yield by Crop by Season', fontweight='bold')
axes[0].set_xlabel('')

pivot_profit = crop_season.pivot(index='Crop', columns='Season', values='Avg_Profit') / 1e3
sns.heatmap(pivot_profit, annot=True, fmt='.0f', cmap='RdYlGn', ax=axes[1],
            linewidths=0.5, cbar_kws={'label': 'Avg Profit (K INR)'}, center=0)
axes[1].set_title('Average Profit (K INR) by Crop by Season', fontweight='bold')
axes[1].set_xlabel('')

plt.tight_layout()
plt.savefig('crop_season_heatmap.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: crop_season_heatmap.png')

# ── Boxplot profit ─────────────────────────────────────────────────────────────
plt.figure(figsize=(16, 6))
sns.boxplot(data=df, x='Season', y='Profit_INR', hue='Crop',
            palette='tab10', flierprops=dict(marker='o', markersize=3, alpha=0.4))
plt.title('Profit Distribution by Season and Crop', fontsize=14, fontweight='bold')
plt.ylabel('Profit (INR)')
plt.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.6)
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', title='Crop')
plt.tight_layout()
plt.savefig('profit_boxplot.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: profit_boxplot.png')

# ── 3. Correlation Matrix ──────────────────────────────────────────────────────
env_cols = ['Rainfall_mm', 'Avg_Temperature_C', 'Humidity_pct', 'Sunlight_Hours_Day',
            'Soil_pH', 'Soil_Moisture_pct', 'Disease_Pest_Risk_pct',
            'Yield_Tonnes_Ha', 'Profit_INR']
corr = df[env_cols].corr()
plt.figure(figsize=(11, 9))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            mask=mask, linewidths=0.5, square=True,
            cbar_kws={'shrink': 0.8, 'label': 'Pearson Correlation'})
plt.title('Correlation Matrix: Environmental Factors vs Outcomes', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_matrix.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: correlation_matrix.png')

# ── Scatter env vs yield ───────────────────────────────────────────────────────
factors = ['Rainfall_mm', 'Avg_Temperature_C', 'Soil_Moisture_pct', 'Sunlight_Hours_Day']
labels  = ['Rainfall (mm)', 'Avg Temperature (C)', 'Soil Moisture (%)', 'Sunlight (hrs/day)']
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Environmental Factors vs Yield (coloured by Season)', fontsize=14, fontweight='bold')
for ax, factor, lbl in zip(axes.flatten(), factors, labels):
    for season, color in SEASON_COLORS.items():
        subset = df[df['Season'] == season]
        ax.scatter(subset[factor], subset['Yield_Tonnes_Ha'], alpha=0.25, s=12, color=color, label=season)
    ax.set_xlabel(lbl)
    ax.set_ylabel('Yield (t/ha)')
    ax.set_title(f'{lbl} vs Yield')
handles = [mpatches.Patch(color=c, label=s) for s, c in SEASON_COLORS.items()]
fig.legend(handles=handles, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.02), title='Season')
plt.tight_layout()
plt.savefig('env_vs_yield.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: env_vs_yield.png')

# ── 4. Resource Usage ──────────────────────────────────────────────────────────
resource_cols = ['Water_Used_m3', 'Fertilizer_kg_ha', 'Pesticide_Litre_ha',
                 'Nitrogen_kg_ha', 'Phosphorus_kg_ha', 'Potassium_kg_ha']
resource = df.groupby('Season')[resource_cols].mean().reset_index()
titles = ['Water Used (m3)', 'Fertilizer (kg/ha)', 'Pesticide (L/ha)',
          'Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)']
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Resource Usage by Season', fontsize=15, fontweight='bold')
for ax, col, title in zip(axes.flatten(), resource_cols, titles):
    colors = [SEASON_COLORS[s] for s in resource['Season']]
    bars = ax.bar(resource['Season'], resource[col], color=colors, edgecolor='white', linewidth=1.5)
    ax.bar_label(bars, fmt='%.1f', padding=3, fontsize=9)
    ax.set_title(title, fontweight='bold')
    ax.set_ylabel(title)
plt.tight_layout()
plt.savefig('resource_usage.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: resource_usage.png')
print(resource.round(2).to_string(index=False))

# ── Water efficiency ───────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Water Efficiency Analysis', fontsize=14, fontweight='bold')
irr_eff = df.groupby('Irrigation_Method')['Water_Efficiency_t_per_1000m3'].mean().sort_values(ascending=False)
irr_eff.plot(kind='bar', ax=axes[0], color='#3498db', edgecolor='white')
axes[0].set_title('Water Efficiency by Irrigation Method', fontweight='bold')
axes[0].set_ylabel('Water Efficiency (t per 1000 m3)')
axes[0].set_xlabel('')
axes[0].tick_params(axis='x', rotation=30)
sns.boxplot(data=df, x='Season', y='Water_Efficiency_t_per_1000m3',
            hue='Irrigation_Method', ax=axes[1], palette='Set2')
axes[1].set_title('Water Efficiency by Season and Irrigation', fontweight='bold')
axes[1].set_ylabel('Water Efficiency (t per 1000 m3)')
axes[1].legend(title='Irrigation', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.tight_layout()
plt.savefig('water_efficiency.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: water_efficiency.png')

# ── 5. State-wise ──────────────────────────────────────────────────────────────
state_perf = df.groupby('State').agg(
    Avg_Yield=('Yield_Tonnes_Ha', 'mean'),
    Avg_Profit=('Profit_INR', 'mean'),
    Total_Production=('Production_Tonnes', 'sum'),
    Farm_Count=('Farm_ID', 'count')
).reset_index().sort_values('Avg_Yield', ascending=False)

fig, axes = plt.subplots(2, 1, figsize=(14, 12))
fig.suptitle('State-wise Agricultural Performance', fontsize=15, fontweight='bold')
top_yield = state_perf.head(10)
axes[0].barh(top_yield['State'], top_yield['Avg_Yield'],
             color=sns.color_palette('viridis', len(top_yield)))
axes[0].set_title('Top 10 States by Average Yield (t/ha)', fontweight='bold')
axes[0].set_xlabel('Average Yield (t/ha)')
axes[0].invert_yaxis()
state_profit = state_perf.sort_values('Avg_Profit', ascending=False).head(10)
colors = ['#2ecc71' if p >= 0 else '#e74c3c' for p in state_profit['Avg_Profit']]
axes[1].barh(state_profit['State'], state_profit['Avg_Profit'] / 1e3, color=colors)
axes[1].set_title('Top 10 States by Average Profit (K INR)', fontweight='bold')
axes[1].set_xlabel('Average Profit (Thousands INR)')
axes[1].axvline(0, color='black', linewidth=0.8)
axes[1].invert_yaxis()
plt.tight_layout()
plt.savefig('state_performance.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: state_performance.png')

# ── 6. NPK ─────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Soil Nutrients (NPK) vs Yield by Season', fontsize=14, fontweight='bold')
for ax, nutrient, label in zip(axes,
    ['Nitrogen_kg_ha', 'Phosphorus_kg_ha', 'Potassium_kg_ha'],
    ['Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)']):
    for season, color in SEASON_COLORS.items():
        subset = df[df['Season'] == season]
        ax.scatter(subset[nutrient], subset['Yield_Tonnes_Ha'], alpha=0.25, s=12, color=color, label=season)
    ax.set_xlabel(label)
    ax.set_ylabel('Yield (t/ha)')
    ax.set_title(f'{label} vs Yield')
handles = [mpatches.Patch(color=c, label=s) for s, c in SEASON_COLORS.items()]
fig.legend(handles=handles, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.04), title='Season')
plt.tight_layout()
plt.savefig('npk_yield.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: npk_yield.png')

# ── Profitability scatter ──────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Profitability Analysis', fontsize=14, fontweight='bold')
for season, color in SEASON_COLORS.items():
    subset = df[df['Season'] == season]
    axes[0].scatter(subset['Yield_Tonnes_Ha'], subset['Profit_INR'] / 1e3, alpha=0.3, s=12, color=color, label=season)
axes[0].axhline(0, color='red', linestyle='--', linewidth=0.8)
axes[0].set_xlabel('Yield (t/ha)')
axes[0].set_ylabel('Profit (Thousands INR)')
axes[0].set_title('Yield vs Profit by Season')
axes[0].legend(title='Season')
for season, color in SEASON_COLORS.items():
    subset = df[df['Season'] == season]
    axes[1].scatter(subset['Seed_Quality_Score'], subset['Yield_Tonnes_Ha'], alpha=0.3, s=12, color=color, label=season)
axes[1].set_xlabel('Seed Quality Score')
axes[1].set_ylabel('Yield (t/ha)')
axes[1].set_title('Seed Quality vs Yield by Season')
axes[1].legend(title='Season')
plt.tight_layout()
plt.savefig('profitability.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: profitability.png')

# ── Disease Risk KDE ───────────────────────────────────────────────────────────
plt.figure(figsize=(10, 5))
for season, color in SEASON_COLORS.items():
    subset = df[df['Season'] == season]['Disease_Pest_Risk_pct']
    subset.plot(kind='kde', label=season, color=color, linewidth=2.5)
plt.title('Disease and Pest Risk Distribution by Season', fontsize=14, fontweight='bold')
plt.xlabel('Disease/Pest Risk (%)')
plt.ylabel('Density')
plt.legend(title='Season')
plt.tight_layout()
plt.savefig('disease_risk.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved: disease_risk.png')

# ── Summary ────────────────────────────────────────────────────────────────────
print('\n=== Best Crop by Yield per Season ===')
print(df.groupby(['Season', 'Crop'])['Yield_Tonnes_Ha'].mean()
       .reset_index().sort_values(['Season', 'Yield_Tonnes_Ha'], ascending=[True, False])
       .groupby('Season').first().reset_index()[['Season', 'Crop', 'Yield_Tonnes_Ha']].to_string(index=False))

print('\n=== Best Crop by Profit per Season ===')
print(df.groupby(['Season', 'Crop'])['Profit_INR'].mean()
       .reset_index().sort_values(['Season', 'Profit_INR'], ascending=[True, False])
       .groupby('Season').first().reset_index()[['Season', 'Crop', 'Profit_INR']].to_string(index=False))

print('\n=== Best Irrigation Method (Water Efficiency) ===')
print(df.groupby('Irrigation_Method')['Water_Efficiency_t_per_1000m3'].mean()
       .sort_values(ascending=False).reset_index().to_string(index=False))

print('\n=== Profitability Rate by Season ===')
for s in df['Season'].unique():
    sub = df[df['Season'] == s]
    profitable_pct = (sub['Profit_INR'] > 0).mean() * 100
    print(f'  {s}: {profitable_pct:.1f}% farms profitable')

print('\nAll charts generated successfully!')
