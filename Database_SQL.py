"""
import sqlite3

def create_database(): 
    conn = sqlite3.connect("1_negozio.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;") #In SQLite3 foreign keys are disabled by default. 
    
    #########################
    # Create tables
    query = '''

    '''

    #########################
    conn.commit()
    conn.close()
"""

import pandas as pd
import sqlite3

def negozio1_database(csv_path, db_path):
    print("🚀 Cargando y procesando el archivo CSV...")
    df = pd.read_csv(csv_path)
    
    # Limpieza inicial: remover columna de índice antigua si existe
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # 1. Conectar a SQLite y activar soporte para Foreign Keys
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("🏗️ Creando tablas relacionales...")

    # Tabla Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        region TEXT
    );
    """)

    # Tabla Productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        category TEXT
    );
    """)

    # Tabla Ventas / Transacciones (Central)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id TEXT PRIMARY KEY,
        customer_id TEXT,
        product_id TEXT,
        transaction_date TEXT,
        units_sold INTEGER,
        discount_applied REAL,
        revenue REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)

    # Tabla Métricas de Marketing (Relación 1:1 o 1:N con Transacciones)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marketing_metrics (
        transaction_id TEXT PRIMARY KEY,
        clicks INTEGER,
        impressions INTEGER,
        conversion_rate REAL,
        ad_ctr REAL,
        ad_cpc REAL,
        ad_spend REAL,
        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
    );
    """)

    print("📥 Insertando datos en las tablas...")

    # Extraer y normalizar entidades únicas para evitar duplicados
    df_customers = df[['Customer_ID', 'Region']].drop_duplicates(subset=['Customer_ID'])
    df_products = df[['Product_ID', 'Category']].drop_duplicates(subset=['Product_ID'])
    
    df_transactions = df[['Transaction_ID', 'Customer_ID', 'Product_ID', 'Transaction_Date', 'Units_Sold', 'Discount_Applied', 'Revenue']]
    df_marketing = df[['Transaction_ID', 'Clicks', 'Impressions', 'Conversion_Rate', 'Ad_CTR', 'Ad_CPC', 'Ad_Spend']]

    # Cargar datos usando Pandas a SQLite aprovechando el mapeo relacional
    df_customers.rename(columns={'Customer_ID': 'customer_id', 'Region': 'region'}).to_sql('customers', conn, if_exists='append', index=False)
    df_products.rename(columns={'Product_ID': 'product_id', 'Category': 'category'}).to_sql('products', conn, if_exists='append', index=False)
    df_transactions.rename(columns={
        'Transaction_ID': 'transaction_id', 'Customer_ID': 'customer_id', 
        'Product_ID': 'product_id', 'Transaction_Date': 'transaction_date', 
        'Units_Sold': 'units_sold', 'Discount_Applied': 'discount_applied', 'Revenue': 'revenue'
    }).to_sql('transactions', conn, if_exists='append', index=False)
    
    df_marketing.rename(columns={
        'Transaction_ID': 'transaction_id', 'Clicks': 'clicks', 'Impressions': 'impressions',
        'Conversion_Rate': 'conversion_rate', 'Ad_CTR': 'ad_ctr', 'Ad_CPC': 'ad_cpc', 'Ad_Spend': 'ad_spend'
    }).to_sql('marketing_metrics', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
    print(f"✨ ¡Éxito! Base de datos relacional creada en '{db_path}' con todas sus dependencias.")


def delete_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Deshabilitar temporalmente las claves foráneas para evitar errores al eliminar tablas
    cursor.execute("PRAGMA foreign_keys = OFF;")
    
    # Lista de tablas a eliminar
    tables = ['marketing_metrics', 'transactions', 'products', 'customers']
    
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")
        print(f"Tabla '{table}' eliminada.")
    
    # Habilitar nuevamente las claves foráneas
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    conn.commit()
    conn.close()
    print(f"Todas las tablas han sido eliminadas de la base de datos '{db_path}'.")