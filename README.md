
# Alan Awards 2024 - Heroes of the Storm Analytics Dashboard

## Overview
A comprehensive analytics dashboard built with Streamlit for analyzing Heroes of the Storm gameplay data. Provides detailed insights into player performance, hero statistics, and game trends through an interactive interface.


## Demo

![alt text](images/ss.png)

[https://aa2024.streamlit.app](https://aa2024.streamlit.app)

## Acknowledgements

- Developed for Alan Awards 2024
- Streamlit visualization framework
- Plotly interactive charts
- Special thanks to the Heroes of the Storm community for their data contributions and support.

## Installation

Clone the repository:

```bash
git clone https://github.com/Lanyev/Dasboard2024AA.git
cd Dasboard2024AA
pip install -r requirements.txt
```

## Usage/Examples

Run the dashboard locally:

```bash
streamlit run moba_dashboard.py
```

Access at [http://localhost:8501](http://localhost:8501)

## Features

- Dynamic Filtering System (Date range selection, Multi-criteria filters for Players, Roles, Maps, Heroes)
- Player performance comparisons (Combat, Economic, Objective statistics)
- Hero performance analysis (Damage/Win rate correlations, Hero-specific metrics)
- Temporal Trends (Daily/hourly performance, Monthly game activity, Historical win rate tracking)
- Competitive Insights (Player rankings, Hero-specific leaderboards, Role-based performance comparisons)


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
