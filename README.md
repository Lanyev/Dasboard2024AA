# Alan Awards 2024 - Heroes of the Storm Analytics Dashboard

## Overview
A comprehensive analytics dashboard built with Streamlit for analyzing Heroes of the Storm gameplay data. This dashboard provides detailed insights into player performance, hero statistics, and game trends through an interactive and visually appealing interface.

## Features

### 🎯 Dynamic Filtering
- Date range selection
- Player filtering
- Role-based filtering
- Map selection
- Hero-specific filtering

### 📊 Key Metrics
- Total games played
- Average hero damage
- Win rates
- Average game duration
- Real-time metric comparisons with historical data

### 🦸‍♂️ Hero Analysis
- Hero performance scatter plots
- Role-based hero distribution treemaps
- Damage vs. win rate correlations
- Hero-specific statistics

### 📈 Temporal Analysis
- Daily performance trends
- Hourly game distribution
- Historical performance tracking
- Win rate trends over time

### 🏆 Rankings
- Top and bottom 5 rankings in various categories:
  - Combat metrics (Hero damage, siege damage, kills, deaths, assists)
  - Economy metrics (Experience, mercenary captures)
  - Objective metrics (Time spent dead, game duration)

## Technical Requirements
- Python 3.7+
- Streamlit
- Pandas
- Plotly Express
- Plotly Graph Objects
- NumPy

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hots-analytics-dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Prepare your data:
- Ensure your CSV file is named `hots_cleaned_data_modified.csv`
- Required columns:
  - GameTime
  - Date
  - Player
  - Role
  - Map
  - Hero
  - Winner
  - HeroDmg
  - SiegeDmg
  - HeroKills
  - Deaths
  - Assists
  - XP
  - MercCaptures
  - SpentDead

## Usage

1. Launch the dashboard:
```bash
streamlit run app.py
```

2. Access the dashboard through your web browser at `http://localhost:8501`

3. Use the sidebar filters to customize your view:
   - Select date ranges
   - Filter by players
   - Choose specific roles
   - Select maps
   - Filter by heroes

## Customization

### Styling
The dashboard includes custom CSS styling with variables for easy theme modification:
- Primary color
- Background color
- Secondary background
- Text color
- Border radius

Modify these variables in the CSS section of the code to customize the appearance.

### Metrics
Add or modify metrics by updating the `metric_categories` dictionary in the `create_rankings` function.

## Contributing
Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License
[Insert your chosen license here]

## Acknowledgments
- Created for Alan Awards 2024
- Built with Streamlit's open-source framework
- Powered by Plotly for data visualization# Dasboard2024AA
