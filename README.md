# Heroes of the Storm Analytics Dashboard

## 🎮 Overview
A comprehensive analytics dashboard built with Streamlit for analyzing Heroes of the Storm gameplay data. Features **multi-dataset support** and **dynamic themes** that adapt to different seasons and tournaments.

### 🆕 New in Version 2.0.0
- **🎯 Multi-Dataset Support**: Switch between different data sources seamlessly
- **🎨 Dynamic Themes**: Visual styles change automatically based on selected dataset
- **🔄 Smart Data Normalization**: Compatible with multiple data formats
- **📊 Real-time Metrics**: Live dataset statistics and comparisons

## 🎨 Available Themes

### 🏆 Alan Awards 2024 Theme
- **Style**: Classic red and gold design
- **Focus**: Retrospective analysis of 2024 tournament
- **Data**: Complete season statistics and player rankings

### 🚀 Temporada 2025 Theme  
- **Style**: Futuristic cyan and blue gradients
- **Focus**: Real-time 2025 season tracking
- **Data**: Latest matches and evolving meta analysis
- **Effects**: Advanced animations and glowing elements


## Demo

![alt text](images/ss.png)

[https://aa2024.streamlit.app](https://aa2024.streamlit.app)

## Acknowledgements

- Developed for Alan Awards 2024
- Streamlit visualization framework
- Plotly interactive charts
- Special thanks to the Heroes of the Storm community for their data contributions and support.

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Lanyev/Dasboard2024AA.git
cd Dasboard2024AA
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Add your data files:**
   - For 2024 data: `hots_cleaned_data_modified.csv`
   - For 2025 data: `hots_cleaned_data_modified_2025_1.csv`
   - The app will auto-detect available datasets

4. **Run the application:**
```bash
streamlit run moba_dashboard.py
```

## 🎯 Usage

1. **Access the dashboard** at [http://localhost:8501](http://localhost:8501)
2. **Select a dataset** from the sidebar dropdown
3. **Watch the theme change** automatically
4. **Apply filters** to focus on specific data
5. **Navigate tabs** for different analysis views
6. **Export insights** using built-in sharing options

## 📁 Data Format Support

### 2024 Format (Alan Awards)
```csv
Player,Hero,Role,Winner,File,Map,Date,GameTime,HeroKills,Assists,Deaths,...
```

### 2025 Format (New Season)  
```csv
PlayerName,HeroName,Winner,FileName,Map,GameTime,HeroKills,Assists,Deaths,...
```

*The application automatically normalizes different formats for seamless compatibility.*

## Features

### 🎯 Multi-Dataset Management
- **Dataset Selection**: Choose between multiple seasons/tournaments
- **Auto-Detection**: Automatically finds available CSV files
- **Theme Switching**: Visual style adapts to selected dataset
- **Data Normalization**: Seamless compatibility between data formats

### 📊 Advanced Analytics
- **Dynamic Filtering System**: Date range, multi-criteria filters for Players, Roles, Maps, Heroes
- **Player Performance**: Combat, Economic, Objective statistics comparisons
- **Hero Analysis**: Damage/Win rate correlations, Hero-specific metrics
- **Temporal Trends**: Daily/hourly performance, Monthly activity, Historical win rate tracking
- **Competitive Insights**: Player rankings, Hero leaderboards, Role-based comparisons

### 🎨 Visual Experience
- **Responsive Design**: Works on desktop and mobile
- **Interactive Charts**: Plotly-powered visualizations
- **Custom Themes**: Two distinct visual styles
- **Smooth Animations**: Enhanced user experience with transitions

### 📊 **Data Validation & Quality**
- **Format Detection**: Automatically detects and normalizes different CSV formats
- **Column Mapping**: Smart mapping between different column naming conventions
- **Missing Data Handling**: Intelligent filling of missing role assignments

### 🔧 **Data Quality Improvements**
- **Hero Role Mapping**: 100% accurate role assignment with automatic corrections
- **Data Cleaning**: Smart detection and correction of data entry errors
- **Encoding Fixes**: Automatic handling of UTF-8 encoding issues in hero names
- **Name Normalization**: Automatic mapping between Spanish/English hero names


## Run Locally

Clone the project:

```bash
  git clone https://github.com/Lanyev/Dasboard2024AA.git
```

Go to the project directory:

```bash
  cd Dasboard2024AA
```

Install dependencies:

```bash
  pip install -r requirements.txt
```

Start the server:

```bash
  streamlit run moba_dashboard.py
```

## Tech Stack

**Client:** Streamlit

**Server:** Python 3.11

**Libraries/Frameworks:** Pandas, Numpy, Plotly Express, Plotly Graph Objects


## Authors

- [@Alan Yeverino](https://www.github.com/Lanyev)

## FAQ

#### How can I filter data by specific players or heroes?

You can use the dynamic filtering system to select players, heroes, roles, or maps, and see real-time updates based on your choices.

#### How do I customize the styling?

Modify the CSS variables in `utils/styles.py` to adjust the colors, themes, and text formatting to your preferences.
