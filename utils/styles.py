import streamlit as st


def apply_styles(theme="alan_awards_2024"):
    """Aplica estilos según el tema seleccionado"""
    if theme == "temporada_2025":
        apply_2025_theme()
    else:
        apply_2024_theme()


def apply_2024_theme():
    """Tema original para Alan Awards 2024"""
    st.markdown(
        """
    <style>
    :root {
        --primary-color: #FF4B4B;
        --bg-color: #1a1a1a;
        --secondary-bg: #2d2d2d;
        --text-color: #ffffff;
        --border-radius: 8px;
        --accent-color: #FFD700;
    }
    
    .main {
        background-color: var(--bg-color);
        color: var(--text-color);
    }
    
    .stButton button {
        background-color: var(--primary-color);
        color: var(--text-color);
        border-radius: var(--border-radius);
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }
    
    .custom-card {
        background-color: var(--secondary-bg);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--primary-color);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary-color);
    }
    
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .stDataFrame {
        width: 100% !important;
    }

    .dataframe td, .dataframe th {
        white-space: nowrap;
        padding: 10px 15px;
        text-align: center;
        overflow: visible;
    }

    .stTable {
        width: 100% !important;
    }

    .dataframe {
        background-color: #2d2d2d;
        color: white;
    }

    .dataframe th, .dataframe td {
        max-width: 300px;
        word-wrap: break-word;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def apply_2025_theme():
    """Nuevo tema para Temporada 2025"""
    st.markdown(
        """
    <style>
    :root {
        --primary-color: #00D4AA;
        --bg-color: #0F1419;
        --secondary-bg: #1E2328;
        --text-color: #F0F6FC;
        --border-radius: 12px;
        --accent-color: #58A6FF;
        --gradient-primary: linear-gradient(135deg, #00D4AA 0%, #58A6FF 100%);
    }
    
    .main {
        background: linear-gradient(145deg, #0F1419 0%, #1E2328 50%, #0F1419 100%);
        color: var(--text-color);
    }
    
    .stButton button {
        background: var(--gradient-primary);
        color: var(--text-color);
        border-radius: var(--border-radius);
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 212, 170, 0.4);
    }
    
    .custom-card {
        background: linear-gradient(145deg, #1E2328 0%, #2D3748 100%);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 212, 170, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .custom-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .stDataFrame {
        width: 100% !important;
    }

    .dataframe td, .dataframe th {
        white-space: nowrap;
        padding: 12px 18px;
        text-align: center;
        overflow: visible;
        border-bottom: 1px solid rgba(0, 212, 170, 0.1);
    }

    .stTable {
        width: 100% !important;
    }

    .dataframe {
        background-color: #1E2328;
        color: #F0F6FC;
        border-radius: var(--border-radius);
        overflow: hidden;
    }

    .dataframe th {
        background: var(--gradient-primary);
        color: #0F1419;
        font-weight: 600;
    }

    .dataframe th, .dataframe td {
        max-width: 300px;
        word-wrap: break-word;
    }
    
    /* Estilos especiales para selectbox */
    .stSelectbox > div > div {
        background-color: #1E2328;
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: var(--border-radius);
    }
    
    /* Animaciones */
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(0, 212, 170, 0.5); }
        50% { box-shadow: 0 0 20px rgba(0, 212, 170, 0.8); }
        100% { box-shadow: 0 0 5px rgba(0, 212, 170, 0.5); }
    }
    
    .metric-container {
        animation: glow 3s ease-in-out infinite;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
