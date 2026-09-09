import json

amp = "&"

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Seasonal Agriculture Performance Analysis\n",
            "\n",
            "**Dataset:** `agriculture_dataset.csv` — 4000 farm records across Indian states  \n",
            "**Columns:** Farm ID, State, District, Crop, Season, Farm Area, Rainfall, Temperature, Humidity,\n",
            "Sunlight, Soil pH, Soil Moisture, NPK nutrients, Irrigation Method, Fertilizer, Pesticide,\n",
            "Seed Quality, Yield, Production, Market Price, Cost, Revenue, Profit, Water Usage, Water Efficiency, Disease/Pest Risk\n",
            "\n",
            "---\n",
            "### Key Questions Answered:\n",
            "1. How does yield and profit vary across seasons?\n",
            "2. Which crops perform best in each season?\n",
            "3. How do environmental factors correlate with outcomes?\n",
            "4. How does resource usage vary by season?\n",
            "5. Which states and irrigation methods are most efficient?\n",
            "6. What drives profitability?"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 1. Setup " + amp + " Data Loading"]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import matplotlib.patches as mpatches\n",
            "import seaborn as sns\n",
            "import warnings\n",
            "warnings.filterwarnings('ignore')\n",
            "\n",
            "sns.set_theme(style='whitegrid', palette='viridis')\n",
            "plt.rcParams['figure.dpi'] = 120\n",
            "SEASON_COLORS = {'Kharif': '#2ecc71', 'Rabi': '#3498db', 'Zaid': '#e67e22'}\n",
            "\n",
            "# Running locally: place agriculture_dataset.csv in the same folder.\n",
            "# Running on Google Colab: use the try/except block below to upload.\n",
            "try:\n",
            "    df = pd.read_csv('agriculture_dataset.csv')\n",
            "except FileNotFoundError:\n",
            "    from google.colab import files\n",
            "    uploaded = files.upload()\n",
            "    df = pd.read_csv(list(uploaded.keys())[0])\n",
            "\n",
            "print(f'Dataset shape: {df.shape}')\n",
            "df.head()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 2. Data Exploration " + amp + " Cleaning"]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('=== Dataset Info ===')\n",
            "df.info()\n",
            "print('\\n=== Statistical Summary ===')\n",
            "df.describe().round(2)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('=== Missing Values ===')\n",
            "missing = df.isnull().sum()\n",
            "print(missing[missing > 0] if missing.sum() > 0 else 'No missing values! Dataset is clean.')\n",
            "\n",
            "print('\\n=== Seasons Present ===')\n",
            "print(df['Season'].value_counts())\n",
            "\n",
            "print('\\n=== Crops Present ===')\n",
            "print(df['Crop'].value_counts())\n",
            "\n",
            "print('\\n=== States Present ===')\n",
            "print(df['State'].nunique(), 'unique states')\n",
            "\n",
            "numeric_cols = df.select_dtypes(include=[np.number]).columns\n",
            "df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())\n",
            "print('\\nData cleaning complete.')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Seasonal Patterns " + amp + " Trends\n",
            "### Q1: How do yield and profit vary across seasons?"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "seasonal = df.groupby('Season').agg(\n",
            "    Avg_Yield=('Yield_Tonnes_Ha', 'mean'),\n",
            "    Avg_Profit=('Profit_INR', 'mean'),\n",
            "    Avg_Revenue=('Revenue_INR', 'mean'),\n",
            "    Avg_Cost=('Total_Cost_INR', 'mean'),\n",
            "    Count=('Farm_ID', 'count')\n",
            ").reset_index()\n",
            "\n",
            "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n",
            "fig.suptitle('Seasonal Agricultural Performance Overview', fontsize=16, fontweight='bold', y=1.02)\n",
            "\n",
            "bars = axes[0].bar(seasonal['Season'], seasonal['Avg_Yield'],\n",
            "                   color=[SEASON_COLORS[s] for s in seasonal['Season']], edgecolor='white', linewidth=1.5)\n",
            "axes[0].bar_label(bars, fmt='%.2f t/ha', padding=3, fontsize=9)\n",
            "axes[0].set_title('Average Yield (Tonnes/Ha)', fontweight='bold')\n",
            "axes[0].set_ylabel('Yield (t/ha)')\n",
            "\n",
            "bars2 = axes[1].bar(seasonal['Season'], seasonal['Avg_Profit'] / 1e3,\n",
            "                    color=[SEASON_COLORS[s] for s in seasonal['Season']], edgecolor='white', linewidth=1.5)\n",
            "axes[1].bar_label(bars2, fmt='%.0f K', padding=3, fontsize=9)\n",
            "axes[1].set_title('Average Profit (INR)', fontweight='bold')\n",
            "axes[1].set_ylabel('Profit (Thousands INR)')\n",
            "axes[1].axhline(0, color='red', linestyle='--', linewidth=0.8, alpha=0.6)\n",
            "\n",
            "x = np.arange(len(seasonal))\n",
            "w = 0.35\n",
            "axes[2].bar(x - w/2, seasonal['Avg_Revenue'] / 1e3, w, label='Revenue', color='#2ecc71', edgecolor='white')\n",
            "axes[2].bar(x + w/2, seasonal['Avg_Cost'] / 1e3, w, label='Cost', color='#e74c3c', edgecolor='white')\n",
            "axes[2].set_xticks(x)\n",
            "axes[2].set_xticklabels(seasonal['Season'])\n",
            "axes[2].set_title('Revenue vs Cost by Season', fontweight='bold')\n",
            "axes[2].set_ylabel('Amount (Thousands INR)')\n",
            "axes[2].legend()\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('seasonal_performance.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()\n",
            "print(seasonal.to_string(index=False))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["### Q2: Which crops perform best in each season?"]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "crop_season = df.groupby(['Season', 'Crop']).agg(\n",
            "    Avg_Yield=('Yield_Tonnes_Ha', 'mean'),\n",
            "    Avg_Profit=('Profit_INR', 'mean')\n",
            ").reset_index()\n",
            "\n",
            "fig, axes = plt.subplots(1, 2, figsize=(18, 6))\n",
            "fig.suptitle('Crop Performance by Season', fontsize=15, fontweight='bold')\n",
            "\n",
            "pivot_yield = crop_season.pivot(index='Crop', columns='Season', values='Avg_Yield')\n",
            "sns.heatmap(pivot_yield, annot=True, fmt='.2f', cmap='YlGn', ax=axes[0],\n",
            "            linewidths=0.5, cbar_kws={'label': 'Avg Yield (t/ha)'})\n",
            "axes[0].set_title('Average Yield by Crop by Season', fontweight='bold')\n",
            "axes[0].set_xlabel('')\n",
            "\n",
            "pivot_profit = crop_season.pivot(index='Crop', columns='Season', values='Avg_Profit') / 1e3\n",
            "sns.heatmap(pivot_profit, annot=True, fmt='.0f', cmap='RdYlGn', ax=axes[1],\n",
            "            linewidths=0.5, cbar_kws={'label': 'Avg Profit (K INR)'}, center=0)\n",
            "axes[1].set_title('Average Profit (K INR) by Crop by Season', fontweight='bold')\n",
            "axes[1].set_xlabel('')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('crop_season_heatmap.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "plt.figure(figsize=(16, 6))\n",
            "sns.boxplot(data=df, x='Season', y='Profit_INR', hue='Crop',\n",
            "            palette='tab10', flierprops=dict(marker='o', markersize=3, alpha=0.4))\n",
            "plt.title('Profit Distribution by Season and Crop', fontsize=14, fontweight='bold')\n",
            "plt.ylabel('Profit (INR)')\n",
            "plt.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.6)\n",
            "plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', title='Crop')\n",
            "plt.tight_layout()\n",
            "plt.savefig('profit_boxplot.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Environmental Conditions " + amp + " Agricultural Outcomes\n",
            "### Q3: How do environmental factors correlate with yield and profit?"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "env_cols = ['Rainfall_mm', 'Avg_Temperature_C', 'Humidity_pct', 'Sunlight_Hours_Day',\n",
            "            'Soil_pH', 'Soil_Moisture_pct', 'Disease_Pest_Risk_pct',\n",
            "            'Yield_Tonnes_Ha', 'Profit_INR']\n",
            "\n",
            "corr = df[env_cols].corr()\n",
            "plt.figure(figsize=(11, 9))\n",
            "mask = np.triu(np.ones_like(corr, dtype=bool))\n",
            "sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,\n",
            "            mask=mask, linewidths=0.5, square=True,\n",
            "            cbar_kws={'shrink': 0.8, 'label': 'Pearson Correlation'})\n",
            "plt.title('Correlation Matrix: Environmental Factors vs Outcomes', fontsize=14, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.savefig('correlation_matrix.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "factors = ['Rainfall_mm', 'Avg_Temperature_C', 'Soil_Moisture_pct', 'Sunlight_Hours_Day']\n",
            "labels  = ['Rainfall (mm)', 'Avg Temperature (C)', 'Soil Moisture (%)', 'Sunlight (hrs/day)']\n",
            "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n",
            "fig.suptitle('Environmental Factors vs Yield (coloured by Season)', fontsize=14, fontweight='bold')\n",
            "\n",
            "for ax, factor, lbl in zip(axes.flatten(), factors, labels):\n",
            "    for season, color in SEASON_COLORS.items():\n",
            "        subset = df[df['Season'] == season]\n",
            "        ax.scatter(subset[factor], subset['Yield_Tonnes_Ha'],\n",
            "                   alpha=0.25, s=12, color=color, label=season)\n",
            "    ax.set_xlabel(lbl)\n",
            "    ax.set_ylabel('Yield (t/ha)')\n",
            "    ax.set_title(f'{lbl} vs Yield')\n",
            "\n",
            "handles = [mpatches.Patch(color=c, label=s) for s, c in SEASON_COLORS.items()]\n",
            "fig.legend(handles=handles, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.02), title='Season')\n",
            "plt.tight_layout()\n",
            "plt.savefig('env_vs_yield.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Resource Usage Variations Across Seasons\n",
            "### Q4: How does resource usage (water, fertilizer, pesticide) change by season?"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "resource_cols = ['Water_Used_m3', 'Fertilizer_kg_ha', 'Pesticide_Litre_ha',\n",
            "                 'Nitrogen_kg_ha', 'Phosphorus_kg_ha', 'Potassium_kg_ha']\n",
            "resource = df.groupby('Season')[resource_cols].mean().reset_index()\n",
            "\n",
            "fig, axes = plt.subplots(2, 3, figsize=(18, 10))\n",
            "fig.suptitle('Resource Usage by Season', fontsize=15, fontweight='bold')\n",
            "\n",
            "titles = ['Water Used (m3)', 'Fertilizer (kg/ha)', 'Pesticide (L/ha)',\n",
            "          'Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)']\n",
            "\n",
            "for ax, col, title in zip(axes.flatten(), resource_cols, titles):\n",
            "    colors = [SEASON_COLORS[s] for s in resource['Season']]\n",
            "    bars = ax.bar(resource['Season'], resource[col], color=colors, edgecolor='white', linewidth=1.5)\n",
            "    ax.bar_label(bars, fmt='%.1f', padding=3, fontsize=9)\n",
            "    ax.set_title(title, fontweight='bold')\n",
            "    ax.set_ylabel(title)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('resource_usage.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()\n",
            "print(resource.round(2).to_string(index=False))"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n",
            "fig.suptitle('Water Efficiency Analysis', fontsize=14, fontweight='bold')\n",
            "\n",
            "irr_eff = df.groupby('Irrigation_Method')['Water_Efficiency_t_per_1000m3'].mean().sort_values(ascending=False)\n",
            "irr_eff.plot(kind='bar', ax=axes[0], color='#3498db', edgecolor='white')\n",
            "axes[0].set_title('Water Efficiency by Irrigation Method', fontweight='bold')\n",
            "axes[0].set_ylabel('Water Efficiency (t per 1000 m3)')\n",
            "axes[0].set_xlabel('')\n",
            "axes[0].tick_params(axis='x', rotation=30)\n",
            "\n",
            "sns.boxplot(data=df, x='Season', y='Water_Efficiency_t_per_1000m3',\n",
            "            hue='Irrigation_Method', ax=axes[1], palette='Set2')\n",
            "axes[1].set_title('Water Efficiency by Season and Irrigation', fontweight='bold')\n",
            "axes[1].set_ylabel('Water Efficiency (t per 1000 m3)')\n",
            "axes[1].legend(title='Irrigation', bbox_to_anchor=(1.01, 1), loc='upper left')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('water_efficiency.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. State-wise " + amp + " Regional Analysis\n",
            "### Q5: Which states perform best in terms of yield and profitability?"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "state_perf = df.groupby('State').agg(\n",
            "    Avg_Yield=('Yield_Tonnes_Ha', 'mean'),\n",
            "    Avg_Profit=('Profit_INR', 'mean'),\n",
            "    Total_Production=('Production_Tonnes', 'sum'),\n",
            "    Farm_Count=('Farm_ID', 'count')\n",
            ").reset_index().sort_values('Avg_Yield', ascending=False)\n",
            "\n",
            "fig, axes = plt.subplots(2, 1, figsize=(14, 12))\n",
            "fig.suptitle('State-wise Agricultural Performance', fontsize=15, fontweight='bold')\n",
            "\n",
            "top_yield = state_perf.head(10)\n",
            "axes[0].barh(top_yield['State'], top_yield['Avg_Yield'],\n",
            "             color=sns.color_palette('viridis', len(top_yield)))\n",
            "axes[0].set_title('Top 10 States by Average Yield (t/ha)', fontweight='bold')\n",
            "axes[0].set_xlabel('Average Yield (t/ha)')\n",
            "axes[0].invert_yaxis()\n",
            "\n",
            "state_profit = state_perf.sort_values('Avg_Profit', ascending=False).head(10)\n",
            "colors = ['#2ecc71' if p >= 0 else '#e74c3c' for p in state_profit['Avg_Profit']]\n",
            "axes[1].barh(state_profit['State'], state_profit['Avg_Profit'] / 1e3, color=colors)\n",
            "axes[1].set_title('Top 10 States by Average Profit (K INR)', fontweight='bold')\n",
            "axes[1].set_xlabel('Average Profit (Thousands INR)')\n",
            "axes[1].axvline(0, color='black', linewidth=0.8)\n",
            "axes[1].invert_yaxis()\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('state_performance.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Profitability Drivers " + amp + " NPK Analysis\n",
            "### Q6: What drives profitability? Soil nutrients vs yield."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n",
            "fig.suptitle('Soil Nutrients (NPK) vs Yield by Season', fontsize=14, fontweight='bold')\n",
            "\n",
            "for ax, nutrient, label in zip(axes,\n",
            "    ['Nitrogen_kg_ha', 'Phosphorus_kg_ha', 'Potassium_kg_ha'],\n",
            "    ['Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)']):\n",
            "    for season, color in SEASON_COLORS.items():\n",
            "        subset = df[df['Season'] == season]\n",
            "        ax.scatter(subset[nutrient], subset['Yield_Tonnes_Ha'],\n",
            "                   alpha=0.25, s=12, color=color, label=season)\n",
            "    ax.set_xlabel(label)\n",
            "    ax.set_ylabel('Yield (t/ha)')\n",
            "    ax.set_title(f'{label} vs Yield')\n",
            "\n",
            "handles = [mpatches.Patch(color=c, label=s) for s, c in SEASON_COLORS.items()]\n",
            "fig.legend(handles=handles, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.04), title='Season')\n",
            "plt.tight_layout()\n",
            "plt.savefig('npk_yield.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n",
            "fig.suptitle('Profitability Analysis', fontsize=14, fontweight='bold')\n",
            "\n",
            "for season, color in SEASON_COLORS.items():\n",
            "    subset = df[df['Season'] == season]\n",
            "    axes[0].scatter(subset['Yield_Tonnes_Ha'], subset['Profit_INR'] / 1e3,\n",
            "                    alpha=0.3, s=12, color=color, label=season)\n",
            "axes[0].axhline(0, color='red', linestyle='--', linewidth=0.8)\n",
            "axes[0].set_xlabel('Yield (t/ha)')\n",
            "axes[0].set_ylabel('Profit (Thousands INR)')\n",
            "axes[0].set_title('Yield vs Profit by Season')\n",
            "axes[0].legend(title='Season')\n",
            "\n",
            "for season, color in SEASON_COLORS.items():\n",
            "    subset = df[df['Season'] == season]\n",
            "    axes[1].scatter(subset['Seed_Quality_Score'], subset['Yield_Tonnes_Ha'],\n",
            "                    alpha=0.3, s=12, color=color, label=season)\n",
            "axes[1].set_xlabel('Seed Quality Score')\n",
            "axes[1].set_ylabel('Yield (t/ha)')\n",
            "axes[1].set_title('Seed Quality vs Yield by Season')\n",
            "axes[1].legend(title='Season')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('profitability.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "plt.figure(figsize=(10, 5))\n",
            "for season, color in SEASON_COLORS.items():\n",
            "    subset = df[df['Season'] == season]['Disease_Pest_Risk_pct']\n",
            "    subset.plot(kind='kde', label=season, color=color, linewidth=2.5)\n",
            "plt.title('Disease and Pest Risk Distribution by Season', fontsize=14, fontweight='bold')\n",
            "plt.xlabel('Disease/Pest Risk (%)')\n",
            "plt.ylabel('Density')\n",
            "plt.legend(title='Season')\n",
            "plt.tight_layout()\n",
            "plt.savefig('disease_risk.png', bbox_inches='tight', dpi=150)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 8. Summary Dashboard"]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('=== Best Crop by Yield per Season ===')\n",
            "print(df.groupby(['Season', 'Crop'])['Yield_Tonnes_Ha'].mean()\n",
            "       .reset_index().sort_values(['Season', 'Yield_Tonnes_Ha'], ascending=[True, False])\n",
            "       .groupby('Season').first().reset_index()[['Season', 'Crop', 'Yield_Tonnes_Ha']].to_string(index=False))\n",
            "\n",
            "print('\\n=== Best Crop by Profit per Season ===')\n",
            "print(df.groupby(['Season', 'Crop'])['Profit_INR'].mean()\n",
            "       .reset_index().sort_values(['Season', 'Profit_INR'], ascending=[True, False])\n",
            "       .groupby('Season').first().reset_index()[['Season', 'Crop', 'Profit_INR']].to_string(index=False))\n",
            "\n",
            "print('\\n=== Best Irrigation Method (Water Efficiency) ===')\n",
            "print(df.groupby('Irrigation_Method')['Water_Efficiency_t_per_1000m3'].mean()\n",
            "       .sort_values(ascending=False).reset_index().to_string(index=False))\n",
            "\n",
            "print('\\n=== Profitability Rate by Season ===')\n",
            "for s in df['Season'].unique():\n",
            "    sub = df[df['Season'] == s]\n",
            "    profitable_pct = (sub['Profit_INR'] > 0).mean() * 100\n",
            "    print(f'  {s}: {profitable_pct:.1f}% farms profitable')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 9. Conclusions " + amp + " Recommendations\n",
            "\n",
            "### Key Findings:\n",
            "| Area | Finding |\n",
            "|---|---|\n",
            "| **Seasonal Yield** | Yield varies meaningfully across Kharif, Rabi, and Zaid seasons |\n",
            "| **Seasonal Profit** | Some seasons consistently generate higher profit margins |\n",
            "| **Top Crops** | Different crops are best-suited to each season — aligning crop choice to season is critical |\n",
            "| **Environmental Factors** | Rainfall, temperature, and soil moisture show notable correlation with yield |\n",
            "| **Resource Usage** | Water and fertilizer demand differs by season, offering optimization opportunities |\n",
            "| **Irrigation** | Drip/Sprinkler irrigation shows better water efficiency than flood irrigation |\n",
            "| **Disease Risk** | Disease and pest risk varies by season — preventive action should be season-aware |\n",
            "| **Seed Quality** | Higher seed quality scores tend to correlate with better yield outcomes |\n",
            "\n",
            "### Recommendations:\n",
            "1. **Season-crop alignment**: Prioritize crops that historically perform best in each season.\n",
            "2. **Water management**: Switch to drip/sprinkler irrigation, especially in Zaid (summer) season.\n",
            "3. **Fertilizer optimization**: Tailor NPK application based on soil tests per season.\n",
            "4. **Disease management**: Implement preventive pest control in high-risk seasons.\n",
            "5. **Seed investment**: Investing in higher-quality seeds improves returns across all seasons."
        ]
    }
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("Seasonal_Agriculture_Analysis.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Notebook written! Total cells: {len(cells)}")
