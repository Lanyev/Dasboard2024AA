import streamlit as st


def create_header():
    st.markdown(
        """
        <h1 style='text-align: center; color: var(--primary-color); margin-bottom: 2rem;'>
            Alan Awards 2024
        </h1>
        """,
        unsafe_allow_html=True,
    )
