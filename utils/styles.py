import streamlit as st


def apply_styles():
    st.markdown(
        """
    <style>
    :root {
        --primary-color: #FF4B4B;
        --bg-color: #1a1a1a;
        --secondary-bg: #2d2d2d;
        --text-color: #ffffff;
        --border-radius: 8px;
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

    /* Estilos específicos para la tabla */
    .stDataFrame {
        width: 100% !important; /* Asegura que la tabla ocupe el 100% del ancho */
    }

    .dataframe td, .dataframe th {
        white-space: nowrap;
        padding: 10px 15px;  /* Ajusta el relleno de las celdas */
        text-align: center;  /* Opcional, ajusta la alineación del texto */
        overflow: visible;   /* Evita que el contenido se corte */
    }

    .stTable {
        width: 100% !important; /* Forzar a que la tabla ocupe el 100% del ancho */
    }

    .dataframe {
        background-color: #2d2d2d;
        color: white;
    }

    /* Agregar un tamaño máximo para las columnas */
    .dataframe th, .dataframe td {
        max-width: 300px;  /* Cambia el valor de max-width si lo necesitas */
        word-wrap: break-word;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
