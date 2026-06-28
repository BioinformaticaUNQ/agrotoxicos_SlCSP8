import pandas as pd

# Archivos de entrada
archivo_1 = "foldseek_human_candidates_preliminar.csv"
archivo_2 = "mejores_alineamientos_foldseek_tmalign.csv"

# Leer CSV
df1 = pd.read_csv(archivo_1)
df2 = pd.read_csv(archivo_2)

# Normalizar nombres para comparar
df1["description_norm"] = df1["description"].astype(str).str.lower().str.strip()
df2["description_norm"] = df2["description"].astype(str).str.lower().str.strip()

# Buscar coincidencias por descripción
repetidas = pd.merge(
    df1,
    df2,
    on="description_norm",
    how="inner",
    suffixes=("_foldseek", "_tmalign")
)

# Seleccionar columnas útiles
columnas = [
    "description_foldseek",
    "target_foldseek",
    "score_foldseek",
    "prob_foldseek",
    "evalue_foldseek",
    "target_tmalign",
    "score_tmalign",
    "prob_tmalign",
    "evalue_tmalign"
]

repetidas_final = repetidas[columnas]

# Guardar resultado
repetidas_final.to_csv("proteinas_repetidas_comparadas.csv", index=False)