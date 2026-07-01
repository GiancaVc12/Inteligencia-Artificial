import pandas as pd

# ==========================================
# ARCHIVO
# ==========================================

archivo = "reporte (1).xls"

# ==========================================
# LEER HTML DISFRAZADO DE XLS
# ==========================================

tablas = pd.read_html(archivo)

df_raw = tablas[0]

# ==========================================
# VER ESTRUCTURA
# ==========================================

print(df_raw.head())

# ==========================================
# CREAR NOMBRES COLUMNAS
# ==========================================

nuevas_columnas = []

for col in df_raw.columns:

    # Primera columna = Fecha
    if col == 0:
        nuevas_columnas.append("Fecha")

    else:
        # Fila 0 suele tener variedad
        variedad = str(df_raw.iloc[0, col]).strip()

        # Fila 1 suele tener tipo de precio
        tipo = str(df_raw.iloc[1, col]).strip()

        # Crear nombre
        nombre = f"{variedad}_{tipo}"

        nuevas_columnas.append(nombre)

# Asignar columnas
df_raw.columns = nuevas_columnas

# ==========================================
# ELIMINAR HEADERS
# ==========================================

df = df_raw.iloc[2:].reset_index(drop=True)

# ==========================================
# CONVERTIR A FORMATO LONG
# ==========================================

df_long = df.melt(
    id_vars=["Fecha"],
    var_name="variedad_precio",
    value_name="precio_promedio_kg"
)

# ==========================================
# EXTRAER SOLO VARIEDAD
# ==========================================

df_long["variedad"] = (
    df_long["variedad_precio"]
    .str.split("_")
    .str[0]
)

# ==========================================
# ELIMINAR AUXILIAR
# ==========================================

df_long = df_long.drop(columns=["variedad_precio"])

# ==========================================
# CONVERTIR FECHA
# ==========================================

df_long["Fecha"] = pd.to_datetime(
    df_long["Fecha"],
    dayfirst=True,
    errors="coerce"
)

# ==========================================
# CONVERTIR PRECIO
# ==========================================

df_long["precio_promedio_kg"] = pd.to_numeric(
    df_long["precio_promedio_kg"],
    errors="coerce"
)

# ==========================================
# LIMPIEZA
# ==========================================

df_long = df_long.dropna(
    subset=["Fecha", "precio_promedio_kg"]
)

# ==========================================
# ORDENAR
# ==========================================

df_long = df_long.sort_values(
    ["Fecha", "variedad"]
).reset_index(drop=True)

# ==========================================
# EXPORTAR CSV
# ==========================================

df_long.to_csv(
    "dataset_precios.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================
# RESULTADO
# ==========================================

print(df_long.head())

print(df_long.shape)