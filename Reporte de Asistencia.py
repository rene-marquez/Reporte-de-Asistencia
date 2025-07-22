import streamlit as st
import pandas as pd

st.title("Reporte de Asistencia")

archivo = st.file_uploader("Selecciona un archivo con extensión CSV", type="csv")

if archivo is not None:
    try:
        # Leer el CSV omitiendo las primeras 4 filas
        df = pd.read_csv(archivo, skiprows=4)

        # Filtrar por valores específicos en la columna "Timetable"
        df_filtrado = df[df['Timetable'].isin(['Mixto', 'Viernes'])].copy()

        if df_filtrado.empty:
            st.warning("No hay filas con 'Timetable' igual a 'Mixto' o 'Viernes'.")
        else:
            # Concatenar las dos primeras columnas para mostrar en el combo
            col1 = df_filtrado.columns[0]
            col2 = df_filtrado.columns[1]

            df_filtrado["identificador"] = df_filtrado[col1].astype(str) + " " + df_filtrado[col2].astype(str)

            seleccion = st.selectbox("Selecciona un registro:", options=df_filtrado["identificador"].tolist())
            
            # Filtrar todas las filas con el identificador seleccionado
            filas_coincidentes = df_filtrado[df_filtrado["identificador"] == seleccion]
            
            # Columnas originales y sus equivalentes en español
            columnas_a_mostrar = {
                "First Name": "Nombre",
                "Last Name": "Apellido",
                "Date": "Fecha",
                "Weekday": "Día de la Semana",
                "Clock-In Time": "Entrada",
                "Clock-Out Time": "Salida",
                "Worked Hours": "Horas Trabajadas",
                "Break Duration": "Duración de Comida"
             }
            # Seleccionar solo las columnas deseadas y renombrarlas
            tabla_mostrar = filas_coincidentes[list(columnas_a_mostrar.keys())].rename(columns=columnas_a_mostrar)

            st.dataframe(tabla_mostrar.reset_index(drop=True))
        
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")