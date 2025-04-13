import streamlit as st
import pandas as pd
import json
import os
import time
from datetime import datetime, timedelta

nombre_excel = "registro_enfoque.xlsx"
nombre_json = "registro_enfoque.json"

if os.path.exists(nombre_json):
    with open(nombre_json, "r") as f:
        registros = json.load(f)
else:
    registros = []

st.set_page_config(page_title="Gestor de Enfoque", layout="centered")
st.title("Gestor de Enfoque y Pausa Activa")

unidad = st.radio("¿Trabajar en minutos o segundos?", ["minutos", "segundos"])
factor = 60 if unidad == "minutos" else 1

actividad = st.text_input("¿Qué actividad vas a realizar?")
inicio_actividad = datetime.now()

tiempo_enfoque = st.number_input(f"¿Cuánto tiempo de enfoque ({unidad})?", min_value=1)
inicio_respuesta_enfoque = datetime.now()
tiempo_pausa = st.number_input(f"¿Cuánto tiempo de pausa activa ({unidad})?", min_value=1)
inicio_respuesta_pausa = datetime.now()

if st.button("Iniciar sesión de enfoque"):
    hora_inicio = datetime.now()
    st.success(f"¡Empieza a enfocarte en '{actividad}'!")
    with st.spinner("Enfoque en curso..."):
        time.sleep(tiempo_enfoque * factor)
    hora_fin = datetime.now()

    duracion = int((hora_fin - hora_inicio).total_seconds())
    registros.append({
        "Actividad": actividad,
        "Inicio": hora_inicio.strftime("%Y-%m-%d %H:%M:%S"),
        "Fin": hora_fin.strftime("%Y-%m-%d %H:%M:%S"),
        "Duración (min:seg)": f"{duracion // 60}:{duracion % 60}",
        "Estado": "Enfoque",
        "Tiempo respuesta enfoque (s)": (inicio_respuesta_enfoque - inicio_actividad).total_seconds(),
        "Tiempo respuesta pausa (s)": (inicio_respuesta_pausa - inicio_respuesta_enfoque).total_seconds()
    })
    st.success("¡Fin del enfoque!")

    if st.checkbox("¿Tomar pausa activa ahora?"):
        st.info(f"Descansa {tiempo_pausa} {unidad}")
        with st.spinner("Pausa activa..."):
            time.sleep(tiempo_pausa * factor)
        hora_fin_pausa = datetime.now()
        duracion_pausa = int((hora_fin_pausa - hora_fin).total_seconds())
        registros.append({
            "Actividad": actividad,
            "Inicio": hora_fin.strftime("%Y-%m-%d %H:%M:%S"),
            "Fin": hora_fin_pausa.strftime("%Y-%m-%d %H:%M:%S"),
            "Duración (min:seg)": f"{duracion_pausa // 60}:{duracion_pausa % 60}",
            "Estado": "Pausa Activa"
        })
        st.success("¡Fin de la pausa!")

    df = pd.DataFrame(registros)
    df.to_excel(nombre_excel, index=False)
    with open(nombre_json, "w") as f:
        json.dump(registros, f, indent=4)

    st.write("**Registro actualizado:**")
    st.dataframe(df)