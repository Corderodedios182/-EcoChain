
"""
Objetivo : unificar los reportes descargados de la plataforma.

Logíca :
    
    Cada archivo tiene un formato diferente de lectura, se cruza la info por la llave N Contrato
    
Mejoras :
    
    - Validar en los días de pagos si el valor de algunas filas es necesario 
    - Transofmar las columnas que tienen un catalogo
    - Pivotear los datos 
    - Ingeniería de características

"""

import pandas as pd
from pathlib import Path

carpeta = Path(r"/Users/carlosrobertofloresluna/Downloads")
######################################
# -- Lectura y union de los contratos#
######################################

#Lectura contratos abiertos
dfs = []
for f in sorted(carpeta.glob("*OpenedAgreements*.xlsx")):
    df = pd.read_excel(f, engine="openpyxl", header=7)
    df["archivo_origen"] = f.name
    dfs.append(df)

df_openedAgreements = pd.concat(dfs, ignore_index=True, sort=False) if dfs else pd.DataFrame()

#Limpieza de datos
mask = df_openedAgreements["Nº contrato"].astype(str).str.contains(r"UBICACIÓN|TOTAL REGISTROS", case=False, na=False)
df_openedAgreements = df_openedAgreements[~mask]

#Lectura contratos cerrados
dfs = []
for f in sorted(carpeta.glob("*ClosedContracts*.xlsx")):
    df = pd.read_excel(f, engine="openpyxl")
    df["archivo_origen"] = f.name
    dfs.append(df)

df_closedContracts = pd.concat(dfs, ignore_index=True, sort=False) if dfs else pd.DataFrame()

#Union de datos
df_contratos = df_openedAgreements.merge(
    df_closedContracts,
    how="left",
    left_on="Nº contrato",
    right_on="N.º contrato",
    suffixes=("_opened", "_closed")
)

#Validación de datos
df_contratos.groupby(["archivo_origen_opened","archivo_origen_closed"]).count()

############################################################################
# -- Lectura y union de contratos con dias de pago
############################################################################

#Lectura contratos cerrados
#Revisar los datos de MC, V1, AX, MC que vienen en los archivos
dfs = []
for f in sorted(carpeta.glob("*DailyPayments*.xlsx")):
    df = pd.read_excel(f,
                       engine="openpyxl",
                       header=5)
    df["archivo_origen"] = f.name
    dfs.append(df)

df_DailyPayments = pd.concat(dfs, ignore_index=True, sort=False) if dfs else pd.DataFrame()

#Limpieza de datos

df_DailyPayments = df_DailyPayments.loc[:, ~df_DailyPayments.columns.astype(str).str.contains(r"^Unnamed", case=False, na=False)]

mask = df_DailyPayments["Nombre"].notna()
df_DailyPayments = df_DailyPayments[mask]

#Union de datos
df_contratos_diaspagos = df_contratos.merge(
    df_DailyPayments,
    how="left",
    left_on="Nº contrato",
    right_on="Nº contrato",
    suffixes=("_contratos", "_diaspagos")
)

#Exportando los datos
df_contratos_diaspagos.to_csv(
    r"/Users/carlosrobertofloresluna/Downloads/df_contratos_diaspagos.csv",
    index=False,
    encoding="utf-8-sig"
)







