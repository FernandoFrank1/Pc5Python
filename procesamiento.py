import pandas as pd
import requests

def obtener_tipo_cambio():
    try:
        url = "https://api.apis.net.pe/v1/tipo-cambio-sunat"
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción para errores HTTP
        data = response.json()
        
        # Verificar si 'PEN' y 'USD' están presentes en el diccionario
        if 'PEN' in data and 'USD' in data:
            exchange_rate = data['PEN'] / data['USD']
            return exchange_rate
        else:
            print("No se encontraron datos válidos de tipo de cambio en la respuesta.")
            return None
    except requests.exceptions.RequestException as e:
        print("Error al obtener el tipo de cambio:", e)
        return None

def convertir_a_dolares(monto, tipo_cambio):
    if tipo_cambio is not None:
        return monto / tipo_cambio
    else:
        return None

def limpiar_columnas(ruta_archivo):
    # Carga el archivo Excel en un DataFrame
    df = pd.read_excel(ruta_archivo)

    # Renombrar las columnas
    nombres_columnas = {
        'ID': 'id',
        'CODIGO PAIS': 'codigo_pais',
        'CODIGO ENTIDAD': 'codigo_entidad',
        'UBIGEO': 'ubigeo',
        'SNIP': 'snip',
        'CUI': 'cui',
        'REGION': 'region',
        'PROVINCIA': 'provincia',
        'DISTRITO': 'distrito',
        'PROYECTO': 'proyecto',
        'DISPOSITIVO LEGAL': 'dispositivo_legal',
        'AMBITO': 'ambito',
        'UNIDAD EJECUTORA': 'unidad_ejecutora',
        'TOTAL EMPLEOS': 'total_empleos',
        'POBLACION BENEFICIARIA': 'poblacion_beneficiaria',
        'TIPOLOGIA': 'tipologia',
        'TIPO MONEDA': 'tipo_moneda',
        'MONTO DE INVERSION': 'monto_inversion',
        'MONTO DE TRANSFERENCIA 2020': 'monto_transferencia_2020',
        'ESTADO': 'estado'
    }

    # Renombrar las columnas y limpiar los nombres
    df.rename(columns=nombres_columnas, inplace=True)
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    # Eliminar columnas duplicadas
    df = df.loc[:, ~df.columns.duplicated()]

    # Verificar si la columna 'DISPOSITIVO LEGAL' está presente
    if 'dispositivo_legal' in df.columns:
        # Eliminar la coma (',') de la columna 'dispositivo_legal'
        df['dispositivo_legal'] = df['dispositivo_legal'].str.replace(',', '')

    # Obtener el tipo de cambio actual
    tipo_cambio = obtener_tipo_cambio()

    # Verificar si se pudo obtener el tipo de cambio
    if tipo_cambio is not None:
        # Convertir los montos de inversión y transferencia a dólares
        df['monto_inversion_dolares'] = df['monto_inversion'].apply(convertir_a_dolares, args=(tipo_cambio,))
        df['monto_transferencia_2020_dolares'] = df['monto_transferencia_2020'].apply(convertir_a_dolares, args=(tipo_cambio,))
    else:
        print("No se pudo obtener el tipo de cambio.")

    # Mostrar solo las primeras filas del DataFrame
    print(df.head())

# Ruta del archivo
ruta_archivo = 'data/reactiva.xlsx'

# Llamar a la función y mostrar solo las primeras filas del DataFrame limpio
limpiar_columnas(ruta_archivo)

