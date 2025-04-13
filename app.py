import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Gestor de Enfoque", layout="centered")
st.title("Gestor de Enfoque y Pausa Activa (versión web optimizada)")

unidad = st.radio("¿Trabajar en minutos o segundos?", ["minutos", "segundos"])
factor = 60 if unidad == "minutos" else 1

actividad = st.text_input("¿Qué actividad vas a realizar?")
tiempo_enfoque = st.number_input(f"¿Cuánto tiempo de enfoque ({unidad})?", min_value=1)
tiempo_pausa = st.number_input(f"¿Cuánto tiempo de pausa activa ({unidad})?", min_value=1)

if st.button("Iniciar sesión de enfoque"):
    tiempo_total = tiempo_enfoque * factor
    progreso = st.empty()
    barra = st.progress(0, text="Enfoque en curso...")

    st.success(f"¡Empieza a enfocarte en '{actividad}'!")

    inicio = time.time()
    for i in range(tiempo_total):
        time.sleep(1)
        transcurrido = i + 1
        porcentaje = int((transcurrido / tiempo_total) * 100)
        barra.progress(porcentaje, text=f"Enfoque: {transcurrido}/{tiempo_total} segundos")
    st.success("¡Tiempo de enfoque finalizado!")

    if st.checkbox("¿Tomar pausa activa ahora?"):
        tiempo_total_pausa = tiempo_pausa * factor
        barra_pausa = st.progress(0, text="Pausa activa en curso...")
        for i in range(tiempo_total_pausa):
            time.sleep(1)
            transcurrido = i + 1
            porcentaje = int((transcurrido / tiempo_total_pausa) * 100)
            barra_pausa.progress(porcentaje, text=f"Pausa: {transcurrido}/{tiempo_total_pausa} segundos")
        st.success("¡Fin de la pausa activa!")

    st.balloons()