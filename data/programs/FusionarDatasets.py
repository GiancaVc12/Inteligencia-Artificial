import pandas as pd

# ==========================================
# LEER CSVs
# ==========================================

df1 = pd.read_csv("dataset_volumen_apurimac_20220101_20233112.csv")
df2 = pd.read_csv("dataset_volumen_apurimac_20240101_20262305.csv")
# ==========================================
# MANTENER MISMAS COLUMNAS
# ==========================================

df2 = df2[df1.columns]

# ==========================================
# UNIR
# ==========================================

df_final = pd.concat(
    [df1, df2],
    ignore_index=True
)

# ==========================================
# LIMPIAR FECHAS
# ==========================================

def convertir_fecha(x):

    x = str(x).strip()

    try:
        # Caso ISO: 2026-05-23
        if "-" in x and len(x.split("-")[0]) == 4:
            return pd.to_datetime(x, format="%Y-%m-%d")

        # Caso normal: 23/05/2026
        elif "/" in x:
            return pd.to_datetime(x, format="%d/%m/%Y")

        else:
            return pd.NaT

    except:
        return pd.NaT

# Aplicar
df_final["Fecha"] = df_final["Fecha"].apply(convertir_fecha)

# ==========================================
# ELIMINAR FECHAS INVÁLIDAS
# ==========================================

df_final = df_final.dropna(subset=["Fecha"])

# ==========================================
# ORDENAR DESCENDENTE
# ==========================================

df_final = df_final.sort_values(
    by="Fecha",
    ascending=False
).reset_index(drop=True)

# ==========================================
# EXPORTAR
# ==========================================


df_final.to_csv(
    "dataset_volumen_apurimac_20220101_20262305.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================
# RESULTADO
# ==========================================

print(df_final.head())

print("\nShape:")
print(df_final.shape)

print("\nColumnas:")
print(df_final.columns.tolist())