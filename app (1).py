import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime

st.set_page_config(page_title="Gestor de Enfoque", layout="centered")
st.title("Gestor de Enfoque y Pausa Activa")

archivo_registro = "registro_enfoque.csv"

# Inicializar archivo CSV si no existe
if not os.path.exists(archivo_registro):
    df_init = pd.DataFrame(columns=["Actividad", "Inicio", "Fin", "Duración", "Estado"])
    df_init.to_csv(archivo_registro, index=False)

# Pestañas de navegación
tab1, tab2 = st.tabs(["Enfoque / Pausa", "Historial"])

with tab1:
    unidad = st.radio("¿Trabajar en minutos o segundos?", ["minutos", "segundos"])
    factor = 60 if unidad == "minutos" else 1

    actividad = st.text_input("¿Qué actividad vas a realizar?")
    tiempo_enfoque = st.number_input(f"¿Cuánto tiempo de enfoque ({unidad})?", min_value=1)
    tiempo_pausa = st.number_input(f"¿Cuánto tiempo de pausa activa ({unidad})?", min_value=1)

    if st.button("Iniciar sesión de enfoque"):
        tiempo_total = tiempo_enfoque * factor
        barra = st.progress(0, text="Enfoque en curso...")

        inicio = datetime.now()
        st.success(f"¡Empieza a enfocarte en '{actividad}'!")
        for i in range(tiempo_total):
            time.sleep(1)
            barra.progress((i + 1) / tiempo_total, text=f"Enfoque: {i + 1}/{tiempo_total} segundos")
        fin = datetime.now()
        st.success("¡Tiempo de enfoque finalizado!")

        duracion = str(fin - inicio).split(".")[0]
        nueva_fila = pd.DataFrame([{
            "Actividad": actividad,
            "Inicio": inicio.strftime("%Y-%m-%d %H:%M:%S"),
            "Fin": fin.strftime("%Y-%m-%d %H:%M:%S"),
            "Duración": duracion,
            "Estado": "Enfoque"
        }])
        nueva_fila.to_csv(archivo_registro, mode='a', header=False, index=False)

        if st.checkbox("¿Tomar pausa activa ahora?"):
            tiempo_total_pausa = tiempo_pausa * factor
            barra_pausa = st.progress(0, text="Pausa activa en curso...")

            inicio_pausa = datetime.now()
            for i in range(tiempo_total_pausa):
                time.sleep(1)
                barra_pausa.progress((i + 1) / tiempo_total_pausa, text=f"Pausa: {i + 1}/{tiempo_total_pausa} segundos")
            fin_pausa = datetime.now()
            st.success("¡Fin de la pausa activa!")

            duracion_pausa = str(fin_pausa - inicio_pausa).split(".")[0]
            nueva_pausa = pd.DataFrame([{
                "Actividad": actividad,
                "Inicio": inicio_pausa.strftime("%Y-%m-%d %H:%M:%S"),
                "Fin": fin_pausa.strftime("%Y-%m-%d %H:%M:%S"),
                "Duración": duracion_pausa,
                "Estado": "Pausa Activa"
            }])
            nueva_pausa.to_csv(archivo_registro, mode='a', header=False, index=False)

        st.balloons()

with tab2:
    st.subheader("Historial de sesiones")
    if os.path.exists(archivo_registro):
        df = pd.read_csv(archivo_registro)
        st.dataframe(df)
        st.download_button("Descargar CSV", df.to_csv(index=False), file_name="registro_enfoque.csv")
    else:
        st.info("Aún no hay sesiones registradas.")