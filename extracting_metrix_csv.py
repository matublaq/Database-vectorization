import sqlite3
import pandas as pd
import numpy as np

################################################################################################################################
# Antes de pedirle a la IA que me arme la base de datos relacional, debo de pasarle las estadísticas de la/s tablas de un .csv #  
################################################################################################################################

###############################
# Estadísticas necesarias: 
#   - Nombre de las columnas. 
#   - Cardinalidad. 
#   - % null. 
#   - Tipo de dato. 
#   - Distribución de valores.
#   etc...
###############################

df = pd.read_csv("Datasets/ecomerce_1.csv")
df.head()
df.info()

df_stats = {}

for column in df.columns: 
    df_stats[column] = {
        "unique": df[column].nunique(),
        "nulls": df[column].isnull().sum(),
        "dtype": df[column].dtype,
        "value_counts": df[column].value_counts().sort_values(ascending=False)
    }
    print(column, 
        "\nunique:", df_stats[column]["unique"], 
        "\nnulls:", df_stats[column]["nulls"], 
        "\ndtype:", df_stats[column]["dtype"], 
        "\nvalue_counts:\nhead(5):", df_stats[column]["value_counts"].head(5), "\ntail(5):", df_stats[column]["value_counts"].tail(5), "\n\n"
    )