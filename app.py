import streamlit as st
import pandas as pd
import time
import os
import json
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Gestor de Enfoque y Pausa", layout="centered")
st.title("Gestor de Enfoque y Pausa Activa")

archivo_csv = "registro_enfoque.csv"
archivo_json = "registro_enfoque.json"

# Cargar historial si existen
if os.path.exists(archivo_csv):
    df_hist = pd.read_csv(archivo_csv)
else:
    df_hist = pd.DataFrame(columns=["Actividad", "Inicio", "Fin", "Duración", "Estado"])
    df_hist.to_csv(archivo_csv, index=False)

# Guardar también en JSON
df_hist.to_json(archivo_json, orient="records", indent=4)

tab1, tab2 = st.tabs(["Enfoque / Pausa", "Historial y Progreso"])

with tab1:
    unidad = st.radio("¿Trabajar en minutos o segundos?", ["minutos", "segundos"])
    factor = 60 if unidad == "minutos" else 1

    actividad = st.text_input("¿Qué actividad vas a realizar?")
    tiempo_enfoque = st.number_input(f"¿Cuánto tiempo de enfoque ({unidad})?", min_value=1)
    tiempo_pausa = st.number_input(f"¿Cuánto tiempo de pausa activa ({unidad})?", min_value=1)

    iniciar = st.button("Iniciar sesión de enfoque")

    if iniciar:
        tiempo_total = tiempo_enfoque * factor
        barra = st.progress(0)
        inicio = datetime.now()
        mensaje = st.empty()

        for i in range(tiempo_total):
            porcentaje = (i + 1) / tiempo_total
            barra.progress(porcentaje)
            mensaje.markdown(f"Enfoque: **{i+1}/{tiempo_total}** segundos")
            time.sleep(1)

        fin = datetime.now()
        duracion = str(fin - inicio).split(".")[0]
        st.success("¡Tiempo de enfoque finalizado!")

        nueva_fila = {
            "Actividad": actividad,
            "Inicio": inicio.strftime("%Y-%m-%d %H:%M:%S"),
            "Fin": fin.strftime("%Y-%m-%d %H:%M:%S"),
            "Duración": duracion,
            "Estado": "Enfoque"
        }
        df_hist = pd.concat([df_hist, pd.DataFrame([nueva_fila])], ignore_index=True)
        df_hist.to_csv(archivo_csv, index=False)
        df_hist.to_json(archivo_json, orient="records", indent=4)

        if st.checkbox("¿Tomar pausa activa ahora?"):
            tiempo_total_pausa = tiempo_pausa * factor
            barra_pausa = st.progress(0)
            mensaje_pausa = st.empty()
            inicio_pausa = datetime.now()

            for i in range(tiempo_total_pausa):
                porcentaje = (i + 1) / tiempo_total_pausa
                barra_pausa.progress(porcentaje)
                mensaje_pausa.markdown(f"Pausa: **{i+1}/{tiempo_total_pausa}** segundos")
                time.sleep(1)

            fin_pausa = datetime.now()
            duracion_pausa = str(fin_pausa - inicio_pausa).split(".")[0]
            st.success("¡Fin de la pausa activa!")

            pausa_fila = {
                "Actividad": actividad,
                "Inicio": inicio_pausa.strftime("%Y-%m-%d %H:%M:%S"),
                "Fin": fin_pausa.strftime("%Y-%m-%d %H:%M:%S"),
                "Duración": duracion_pausa,
                "Estado": "Pausa Activa"
            }
            df_hist = pd.concat([df_hist, pd.DataFrame([pausa_fila])], ignore_index=True)
            df_hist.to_csv(archivo_csv, index=False)
            df_hist.to_json(archivo_json, orient="records", indent=4)

        st.balloons()

with tab2:
    st.subheader("Historial de sesiones")

    if not df_hist.empty:
        df_hist["Inicio"] = pd.to_datetime(df_hist["Inicio"])
        df_hist["Fecha"] = df_hist["Inicio"].dt.date

        actividad_filtrada = st.selectbox("Filtrar por actividad (opcional)", ["Todas"] + sorted(df_hist["Actividad"].dropna().unique().tolist()))
        if actividad_filtrada != "Todas":
            df_hist = df_hist[df_hist["Actividad"] == actividad_filtrada]

        st.dataframe(df_hist)
        st.download_button("Descargar CSV", df_hist.to_csv(index=False), file_name="registro_enfoque.csv")

        df_enfoque = df_hist[df_hist["Estado"] == "Enfoque"]
        fechas_con_actividad = sorted(df_enfoque["Fecha"].unique(), reverse=True)

        # Calcular racha
        racha = 0
        hoy = datetime.today().date()
        for i, fecha in enumerate(fechas_con_actividad):
            if fecha == hoy - timedelta(days=i):
                racha += 1
            else:
                break
        st.info(f"Racha actual: {racha} día(s) consecutivo(s) con sesiones de enfoque.")

        # Gráfica
        df_enfoque["Duración (min)"] = pd.to_timedelta(df_enfoque["Duración"]).dt.total_seconds() / 60
        resumen = df_enfoque.groupby("Fecha")["Duración (min)"].sum().reset_index()

        st.subheader("Progreso diario (minutos de enfoque)")
        fig = px.bar(resumen, x="Fecha", y="Duración (min)", title="Tiempo de enfoque por día", labels={"Duración (min)": "Minutos"})
        st.plotly_chart(fig)
    else:
        st.info("Aún no hay sesiones registradas.")
