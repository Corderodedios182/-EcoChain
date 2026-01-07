
"""
Objetivo : unificar los reportes descargados de la plataforma.

Logíca :
    
    Cada archivo tiene un formato diferente de lectura, se cruza la info por la llave N Contrato
    
Mejoras :
    
    - Validar en los días de pagos si el valor de algunas filas es necesario 
    - Pivotear los datos 

"""

import pandas as pd

######################################
# -- Lectura y union de los contratos#
######################################

#Lectura contratos abiertos
df_openedAgreements = pd.read_excel(
    r"/Users/carlosrobertofloresluna/Downloads/OpenedAgreements_0725.xlsx",
    engine="openpyxl",
    header=7
)

#Limpieza de datos
mask = df_openedAgreements["Nº contrato"].astype(str).str.contains(r"UBICACIÓN|TOTAL REGISTROS", case=False, na=False)
df_openedAgreements = df_openedAgreements[~mask]
df_openedAgreements['fuente'] = 'contrato abierto'

#Lectura contratos cerrados
df_closedContracts = pd.read_excel(
    r"/Users/carlosrobertofloresluna/Downloads/ClosedContracts_0725.xlsx",
    engine="openpyxl"
)
df_closedContracts['fuente'] = 'contrato cerrados'

#Union de datos
df_contratos = df_openedAgreements.merge(
    df_closedContracts,
    how="left",
    left_on="Nº contrato",
    right_on="N.º contrato",
    suffixes=("_opened", "_closed")
)

############################################################################
# -- Lectura y union de contratos con dias de pago
############################################################################

#Revisar los datos de MC, V1, AX, MC que vienen en los archivos
df_DailyPayments = pd.read_excel(
    r"/Users/carlosrobertofloresluna/Downloads/DailyPayments_0725.xlsx",
    engine="openpyxl",
    header=5)

#Limpieza de datos
df_DailyPayments['fuente'] = 'dias pagos'
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










