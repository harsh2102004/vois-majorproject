# 🌾 Seasonal Agriculture Performance Analysis

> **VOIS AICTE Batch1 2026–2027 | Major Project**

A complete data analytics project analyzing seasonal agricultural performance across Indian states using a dataset of **4,000 farm records** and **28 features**.

---

## 📌 Project Overview

Agricultural activities are influenced by seasonal variations in environmental conditions, farming practices, resource availability and market conditions. This project investigates **how agricultural performance changes across seasons (Kharif, Rabi, Zaid)** by identifying meaningful patterns, trends, relationships and variations within the data.

---

## 📂 Repository Structure

```
vois-majorproject/
├── Seasonal_Agriculture_Analysis.ipynb   # Main executed Jupyter Notebook (with all outputs)
├── agriculture_dataset.csv               # Dataset (4000 rows × 28 columns)
├── README.md                             # This file
├── seasonal_performance.png              # Yield, Profit, Revenue vs Cost by Season
├── crop_season_heatmap.png               # Crop yield & profit heatmaps
├── profit_boxplot.png                    # Profit distribution by season & crop
├── correlation_matrix.png               # Environmental factors correlation
├── env_vs_yield.png                      # Rainfall, Temp, Soil, Sunlight vs Yield
├── resource_usage.png                    # Water, Fertilizer, NPK, Pesticide by season
├── water_efficiency.png                  # Irrigation method efficiency comparison
├── state_performance.png                 # Top 10 states by yield & profit
├── npk_yield.png                         # Nitrogen, Phosphorus, Potassium vs Yield
├── profitability.png                     # Yield vs Profit, Seed Quality vs Yield
└── disease_risk.png                      # Disease & pest risk distribution by season
```

---

## 📊 Dataset Description

| Feature | Description |
|---|---|
| `Farm_ID` | Unique farm identifier |
| `State`, `District` | Location (8 Indian states) |
| `Crop` | Crop type (Rice, Wheat, Maize, Cotton, Pulses, Groundnut, Chilli, Sugarcane) |
| `Season` | Kharif / Rabi / Zaid |
| `Farm_Area_Hectares` | Farm size |
| `Rainfall_mm` | Rainfall received |
| `Avg_Temperature_C` | Average temperature |
| `Humidity_pct` | Humidity percentage |
| `Sunlight_Hours_Day` | Daily sunlight hours |
| `Soil_pH`, `Soil_Moisture_pct` | Soil conditions |
| `Nitrogen_kg_ha`, `Phosphorus_kg_ha`, `Potassium_kg_ha` | NPK nutrients |
| `Irrigation_Method` | Drip / Sprinkler / Flood / Rainfed |
| `Fertilizer_kg_ha`, `Pesticide_Litre_ha` | Input usage |
| `Seed_Quality_Score` | Seed quality rating |
| `Yield_Tonnes_Ha` | Crop yield |
| `Production_Tonnes` | Total production |
| `Market_Price_INR_Tonne` | Market price |
| `Total_Cost_INR`, `Revenue_INR`, `Profit_INR` | Economic outcomes |
| `Water_Used_m3`, `Water_Efficiency_t_per_1000m3` | Water usage |
| `Disease_Pest_Risk_pct` | Disease & pest risk |

---

## 🔍 Key Questions Addressed

1. How does agricultural performance vary across seasons?
2. Which crops perform best in each season?
3. What relationships exist between environmental conditions and agricultural outcomes?
4. How does resource usage vary across seasons?
5. Which states and irrigation methods are most efficient?
6. What drives profitability — seed quality, NPK, or yield?
7. Are seasonal patterns consistent across different regions?
8. How do economic outcomes (revenue, cost, profit) differ by season?

---

## 📈 Key Findings

| Area | Finding |
|---|---|
| **Best Season** | **Kharif** — highest avg yield (5.63 t/ha) and avg profit (₹178K) |
| **Worst Season** | **Zaid** — avg profit is **negative** (−₹24K); only 35.5% farms profitable |
| **Top Crop** | **Sugarcane** dominates yield and profit across all seasons |
| **Profitability** | Kharif: 57.8% profitable, Rabi: 48.9%, Zaid: 35.5% |
| **Best Irrigation** | **Rainfed** has highest water efficiency (7.56 t/1000m³), followed by Drip |
| **Zaid Risk** | Zaid uses the most water (6,419 m³) yet delivers the worst profit |
| **Disease Risk** | Risk distributions vary by season — season-aware pest management is critical |

---

## 🧹 Data Cleaning

- **Missing values found:** Rainfall (48), Soil Moisture (40), Yield (32)
- **Strategy:** Filled with column median to preserve distribution
- **Result:** Clean dataset ready for analysis

---

## 📉 Visualizations Produced

| Chart | Description |
|---|---|
| Seasonal Performance | Average Yield, Profit, Revenue vs Cost per season |
| Crop-Season Heatmap | Yield and Profit for each crop across seasons |
| Profit Boxplot | Distribution of profit by season and crop |
| Correlation Matrix | Pearson correlation of environmental factors vs outcomes |
| Environmental Scatter | Rainfall, Temperature, Soil Moisture, Sunlight vs Yield |
| Resource Usage | Water, Fertilizer, Pesticide, NPK bar charts by season |
| Water Efficiency | By irrigation method and season |
| State Performance | Top 10 states by yield and profit |
| NPK vs Yield | Nitrogen, Phosphorus, Potassium scatter plots |
| Profitability | Yield vs Profit and Seed Quality vs Yield |
| Disease Risk | KDE distribution of pest risk by season |

---

## 💡 Recommendations

1. **Season-crop alignment** — Prioritize Sugarcane in Kharif for maximum returns
2. **Avoid Zaid for resource-heavy crops** — High water cost with negative avg profit
3. **Switch to Drip/Rainfed irrigation** — Significantly better water efficiency
4. **Tailor NPK application** — Based on soil tests per season to reduce waste
5. **Invest in seed quality** — Higher seed scores consistently yield better outcomes
6. **Season-aware pest management** — Disease risk distribution differs by season

---

## 🚀 Running Locally

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scipy jupyter
```

### Steps
```bash
git clone https://github.com/harsh2102004/vois-majorproject.git
cd vois-majorproject
jupyter notebook Seasonal_Agriculture_Analysis.ipynb
```
> The notebook will load `agriculture_dataset.csv` automatically from the same folder.

---

## ☁️ Running on Google Colab

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Click **GitHub** tab → enter `harsh2102004/vois-majorproject`
3. Select `Seasonal_Agriculture_Analysis.ipynb`
4. Upload `agriculture_dataset.csv` via the **Files** panel (folder icon on left sidebar)
5. Run all cells (**Runtime → Run all**)

> The notebook automatically detects Colab and will prompt you to upload the file if it's not found.

---

## 🛠️ Technologies Used

| Tool | Purpose |
|---|---|
| Python 3 | Core programming language |
| Pandas | Data loading, cleaning, aggregation |
| NumPy | Numerical operations |
| Matplotlib | Base plotting |
| Seaborn | Statistical visualizations |
| Jupyter Notebook | Interactive analysis environment |
| Git + GitHub | Version control and hosting |

---

## 👥 Team

**VOIS AICTE Batch1 2026–2027**  
GitHub: [harsh2102004/vois-majorproject](https://github.com/harsh2102004/vois-majorproject)
