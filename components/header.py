import streamlit as st


def create_header(title="Alan Awards 2024"):
    """Crea un header dinámico según el título proporcionado"""
    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: var(--primary-color); margin: 0; font-size: 3rem; font-weight: 700;'>
                {title}
            </h1>
            <p style='color: var(--text-color); font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.8;'>
                Dashboard de Análisis Interactivo
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
