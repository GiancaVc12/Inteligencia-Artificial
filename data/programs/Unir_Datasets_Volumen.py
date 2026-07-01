import pandas as pd
import glob
import os

# ==========================================
# CARPETA DONDE ESTÁN LOS CSV
# ==========================================

carpeta = r"D:\PUCP\Datasets\Papa\Volumen\Zonas\Zonas_Procesadas"

# ==========================================
# BUSCAR TODOS LOS CSV
# ==========================================

archivos = glob.glob(os.path.join(carpeta, "*.csv"))

print(f"Archivos encontrados: {len(archivos)}")

# ==========================================
# LEER Y GUARDAR DATAFRAMES
# ==========================================

lista_dfs = []

for archivo in archivos:

    print(f"Leyendo: {archivo}")

    df = pd.read_csv(archivo)

    lista_dfs.append(df)

# ==========================================
# UNIR TODOS LOS DATASETS
# ==========================================

df_unificado = pd.concat(
    lista_dfs,
    ignore_index=True
)

# ==========================================
# CONVERTIR FECHA
# ==========================================

df_unificado["Fecha"] = pd.to_datetime(
    df_unificado["Fecha"],
    format="mixed"
)

# ==========================================
# ORDENAR
# Fecha -> variedad -> Region -> zona
# TODO DESCENDENTE
# ==========================================

df_unificado = df_unificado.sort_values(
    by=["Fecha", "variedad", "Region", "zona"],
    ascending=[False, False, False, False]
).reset_index(drop=True)

# ==========================================
# EXPORTAR CSV FINAL
# ==========================================

ruta_salida = os.path.join(
    carpeta,
    "dataset_unificado_volumen_total.csv"
)

df_unificado.to_csv(
    ruta_salida,
    index=False,
    encoding="utf-8-sig"
)

# ==========================================
# RESULTADO
# ==========================================

print("\nDataset unificado generado correctamente")

print(df_unificado.head())

print("\nShape:")
print(df_unificado.shape)