import pandas as pd
import glob
import os

# Carpeta donde están tus nuevos CSVs ya procesados
carpeta = r"D:\PUCP\Datasets\Papa\Clima_Zonas\1_Datasets_Zonas"  # Cambia la ruta si están en otra carpeta
archivo_final = "Consolidado_Clima_Zonas.csv"

# Buscar todos los archivos CSV en la carpeta
archivos = glob.glob(os.path.join(carpeta, "*.csv"))

# Lista para almacenar los DataFrames
lista_df = []

print(f"Se encontraron {len(archivos)} archivos para unir.")

for archivo in archivos:
    # Ignorar el archivo final si ya existe en la misma carpeta para no duplicar datos
    if os.path.basename(archivo) == archivo_final:
        continue

    # Leer el CSV (ya no saltamos líneas porque estos archivos ya están procesados)
    df = pd.read_csv(archivo)

    # Convertir la columna FECHA a datetime para asegurar un ordenamiento cronológico correcto
    if "FECHA" in df.columns:
        df["FECHA"] = pd.to_datetime(df["FECHA"])

    lista_df.append(df)

# Unir todos los DataFrames en uno solo
df_consolidado = pd.concat(lista_df, ignore_index=True)

# Eliminar duplicados si es que se repiten filas entre archivos
df_consolidado = df_consolidado.drop_duplicates()

# ORDENAR DE FORMA DESCENDENTE: 1° FECHA, 2° region, 3° zona
# Usamos ascending=False para que sea descendente en las tres columnas
df_consolidado = df_consolidado.sort_values(
    by=["FECHA", "region", "zona"],
    ascending=[False, False, False]
).reset_index(drop=True)

# Asegurar el orden exacto de las columnas que solicitaste
columnas_ordenadas = [
    "region",
    "zona",
    "FECHA",
    "YEAR",
    "DOY",
    "T2M",
    "T2M_MIN",
    "T2M_MAX",
    "IMERG_PRECTOT",
    "dias_con_helada_en_cultivo"
]

# Reindexamos por si algún archivo tenía columnas extra
df_consolidado = df_consolidado[columnas_ordenadas]

# Guardar el CSV consolidado final
salida = os.path.join(carpeta, archivo_final)
df_consolidado.to_csv(salida, index=False)

print("\n¡Proceso completado exitosamente!")
print(f"Archivo consolidado guardado en: {salida}")
print(f"Cantidad total de registros combinados: {len(df_consolidado)}")

print("\nMuestra de los primeros registros (Fechas más recientes primero):")
print(df_consolidado.head())