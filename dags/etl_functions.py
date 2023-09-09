## Libraries and frameworks
import pandas as pd
import numpy as np
import requests 
import psycopg2
#from dotenv import load_dotenv
#import os
#load_dotenv("config.env")
from airflow.models import Variable


        ############################################################################## PARTE 1: FUNCIONES Y DATA:
def extract_transform_load():
    def get_weather_data(lat, lon, api_key):
        """
        Obtiene datos climáticos de la API OpenWeatherMap para una latitud y longitud dadas del día en el que se ejecuta.
        Args:
            lat (float): Latitud de la ubicación.
            lon (float): Longitud de la ubicación.
            api_key (str): Tu clave de API para acceder a la API de OpenWeatherMap.
        Return:
            pd.DataFrame o None: Un DataFrame que contiene los datos climáticos si la llamada a la API es exitosa,
            de lo contrario, devuelve None. El DataFrame incluye información como la ubicación, temperatura,
            humedad, velocidad del viento y más.
        """
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200:
            weather_data = {
                "Location": data["name"],
                "Latitude": data["coord"]["lat"],
                "Longitude": data["coord"]["lon"],
                "Temperature": data["main"]["temp"],
                "Feels Like": data["main"]["feels_like"],
                "Pressure": data["main"]["pressure"],
                "Humidity": data["main"]["humidity"],
                "Weather": data["weather"][0]["main"],
                "Description": data["weather"][0]["description"],
                "Wind Speed": data["wind"]["speed"],
                "Wind Direction": data["wind"]["deg"],
                "Cloudiness": data["clouds"]["all"],
                "Visibility": data.get("visibility", None),
                "Sunrise": pd.to_datetime(data["sys"]["sunrise"], unit="s"),
                "Sunset": pd.to_datetime(data["sys"]["sunset"], unit="s"),
            }
            df = pd.DataFrame([weather_data])
            return df
        else:
            print("Error fetching weather data.")
            return None
    ## --------------------------------------------------------------------------------------------

    ## -------- Datos para crear el Dataframe con el que se hará la consulta cada día para traer los datos de las capitales de América del Sur
    data = {
        "Country": ["Argentina", "Bolivia", "Brasil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Perú", "Surinam", "Uruguay", "Venezuela"],
        "Capital": ["Buenos Aires", "La Paz", "Brasilia", "Santiago", "Bogotá", "Quito", "Georgetown", "Asunción", "Lima", "Paramaribo", "Montevideo", "Caracas"],
        "Latitud": [-34.6118, -16.5004, -15.7801, -33.4489, 4.6097, -0.1807, 6.9271, -25.2637, -12.0464, 5.8664, -34.8941, 10.4961],
        "Longitud": [-58.4173, -68.1500, -47.9292, -70.6693, -74.0817, -78.4678, -58.1530, -57.5759, -77.0428, -55.1668, -56.0675, -66.8819]
    }
    ## --------------------------------------------------------------------------------------------

    ## -------- Establecer conexión con redshift
    #host = os.getenv("HOST")
    #port = os.getenv("PORT")
    #user = os.getenv("USER")
    #password = os.getenv("PASSWORD")
    #database = os.getenv("DATABASE")

    host = Variable.get("HOST")
    port = Variable.get("PORT")
    user = Variable.get("USER")
    password = Variable.get("PASSWORD")
    database = Variable.get("DATABASE")

    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )
    ## --------------------------------------------------------------------------------------------


    ############################################################################## PARTE 2: PROCESO ETL

    #### EXRACT 📥 

    #token = os.getenv("TOKEN")
    token = Variable.get("TOKEN")

    # Crear un dataframe con las coordenadas de las capitales sudamericanas para consultar a la API
    df = pd.DataFrame(data)

    # Agregar columna con la fecha actual
    current_date = pd.to_datetime('today').date()
    df['Date'] = current_date

    # Agregar columna "id" con la calve combinada de fecha y las 3 primeras letras del nombre de la capital
    df['id'] = df['Capital'].str.replace(" ", "").str[:3].str.upper() + current_date.strftime('%Y%m%d')

    # Aplicar la función a cada fila del DataFrame
    weather_data_list = []
    for index, row in df.iterrows():
        weather_data = get_weather_data(row['Latitud'], row['Longitud'], token)
        if weather_data is not None:
            weather_data_list.append(weather_data)

    # Crear un nuevo DataFrame con los datos climáticos
    weather_df = pd.concat(weather_data_list, ignore_index=True)
    result_df = pd.concat([df, weather_df], axis=1)  # Combinar los DataFrames


    #### TRANSFOR 🔃 

    # Eliminar columnas que no serán cargadas.
    result_df = result_df.drop(columns=['Latitud','Longitud','Location','Latitude','Longitude'])

    # Reordenar el dataframe.
    order = ['id','Date','Country', 'Capital','Temperature', 'Feels Like','Pressure', 'Humidity', 'Weather', 'Description', 'Wind Speed','Wind Direction', 'Cloudiness', 'Visibility', 'Sunrise', 'Sunset']
    result_df = result_df[order]

    #Cambiar el nombre a las columnas que tienen espacio.
    result_df = result_df.rename(columns={'Feels Like':'Feels_Like','Wind Speed':'Wind_Speed','Wind Direction':'Wind_Direction'})



    #### LOAD ➡️💾 

    rows_weather_Data = [tuple(result_df.iloc[i].values) for i in range (result_df.shape[0])]

    new_rows_weather_Data = []

    for tupla in rows_weather_Data:
        nueva_tupla = []
        for valor in tupla:
            if isinstance(valor, np.float64):
                nueva_tupla.append(float(valor))
            elif isinstance(valor, np.int64):
                nueva_tupla.append(int(valor))
            else:
                nueva_tupla.append(valor)
        new_rows_weather_Data.append(tuple(nueva_tupla))

    fill_weather_Data = '''
    INSERT INTO jabrahanba_coderhouse.weather_data (id, Date, Country, Capital, Temperature, Feels_Like, Pressure, Humidity, Weather, Description, Wind_Speed, Wind_Direction, Cloudiness, Visibility, Sunrise, Sunset)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    with conn.cursor() as cursor:
        cursor.executemany(fill_weather_Data, new_rows_weather_Data)
        conn.commit()



