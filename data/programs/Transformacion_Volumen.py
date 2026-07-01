import pandas as pd

# ==========================================
# ARCHIVO
# ==========================================

archivo = "reporte (2).xls"

# ==========================================
# LEER HTML DISFRAZADO DE XLS
# ==========================================

tablas = pd.read_html(archivo)

# Primera tabla
df_raw = tablas[0]

# ==========================================
# CREAR NOMBRES DE COLUMNAS
# ==========================================

nuevas_columnas = []

for col in df_raw.columns:

    # Primera fila -> variedad
    variedad = str(df_raw.iloc[0, col]).strip()

    # Segunda fila -> tipo (Volumen)
    tipo = str(df_raw.iloc[1, col]).strip()

    # Tercera fila -> zona
    zona = str(df_raw.iloc[2, col]).strip()

    # Primera columna = fecha
    if col == 0:
        nuevas_columnas.append("Fecha")

    else:
        nombre = f"{variedad}_{zona}"
        nuevas_columnas.append(nombre)

# Asignar columnas
df_raw.columns = nuevas_columnas

# ==========================================
# ELIMINAR FILAS HEADER
# ==========================================

df = df_raw.iloc[3:].reset_index(drop=True)

# ==========================================
# CONVERTIR FECHA
# ==========================================

df["Fecha"] = pd.to_datetime(
    df["Fecha"],
    dayfirst=True,
    errors="coerce"
)

# ==========================================
# TRANSFORMAR A FORMATO LONG
# ==========================================

df_long = df.melt(
    id_vars=["Fecha"],
    var_name="variedad_zona",
    value_name="volumen"
)

# ==========================================
# SEPARAR VARIEDAD Y ZONA
# ==========================================

df_long[["variedad", "zona"]] = (
    df_long["variedad_zona"]
    .str.split("_", n=1, expand=True)
)

# ==========================================
# ELIMINAR COLUMNA AUXILIAR
# ==========================================

df_long = df_long.drop(columns=["variedad_zona"])

# ==========================================
# CONVERTIR VOLUMEN A NUMÉRICO
# ==========================================

df_long["volumen"] = pd.to_numeric(
    df_long["volumen"],
    errors="coerce"
)

# ==========================================
# LIMPIEZA
# ==========================================

# Eliminar NaN
df_long = df_long.dropna(subset=["volumen"])

# Eliminar ceros
df_long = df_long[df_long["volumen"] != 0]

# Eliminar filas TOTAL
df_long = df_long[
    ~df_long["zona"]
    .str.contains("total", case=False, na=False)
]

# ==========================================
# ORDENAR
# ==========================================

df_long = df_long.sort_values(
    ["Fecha", "variedad", "zona"]
).reset_index(drop=True)

# ==========================================
# EXPORTAR CSV
# ==========================================

df_long.to_csv(
    "dataset_volumen_apurimac_20220101_20233112.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================
# RESULTADO
# ==========================================

print(df_long.head())

print("\nShape:")
print(df_long.shape)

print("\nColumnas:")
print(df_long.columns)