# Proyecto de Automatización de ETL con Airflow y Amazon Redshift 🚀

El objetivo del proyecto fue crear una aplicación que hiciera un proceso de ETL y se automatizara con airflow para que se ejecute periódicamente cargando una base de datos en amazon redshift. 😎

## Tecnologías Utilizadas 🛠️

| Tecnología       | Descripción                                           |
|------------------|-------------------------------------------------------|
| Python           | El lenguaje de programación principal.                |
| Pandas           | Biblioteca de análisis de datos en Python.            |
| Requests         | Para realizar consultas a la API externa.            |
| Airflow          | Plataforma de programación de flujo de trabajo.       |
| Amazon Redshift  | Servicio de almacenamiento de datos en la nube.      |
| Docker           | Para contenerizar la aplicación.                     |
| Psycopg2         | Biblioteca para interactuar con PostgreSQL (Redshift).|

## Open Weather API 🌦️

En este proyecto, utilizamos la Open Weather API para obtener datos meteorológicos de las principales ciudades de Sudamérica. Realizamos una consulta diaria para extraer información relevante.

### Ciudades Principales 🏙️

- Buenos Aires 🇦🇷
- La Paz 🇧🇴
- Brasilia 🇧🇷
- Santiago 🇨🇱
- Bogotá 🇨🇴
- Quito 🇪🇨
- Georgetown 🇬🇾
- Asunción 🇵🇾
- Lima 🇵🇪
- Paramaribo 🇸🇷
- Montevideo 🇺🇾
- Caracas 🇻🇪

### Campos Extraídos 🌡️

A continuación, se presentan los campos que extraemos de la API para cada ciudad:

| Campo           | Descripción                                        |
|-----------------|----------------------------------------------------|
| Country         | País al que pertenece la ciudad.                 |
| Capital         | Si la ciudad es la capital del país.             |
| Date            | Fecha de la consulta.                             |
| id              | Identificador único (ciudad + fecha).            |
| Temperature     | Temperatura actual en °C.                         |
| Feels Like      | Sensación térmica en °C.                          |
| Pressure        | Presión atmosférica en hPa.                       |
| Humidity        | Humedad relativa en %.                            |
| Weather         | Estado del tiempo (ejemplo: Rain, Clouds, Clear).|
| Description     | Descripción detallada del estado del tiempo.     |
| Wind Speed      | Velocidad del viento en m/s.                     |
| Wind Direction  | Dirección del viento en grados.                  |
| Cloudiness      | Cobertura de nubes en %.                         |
| Visibility      | Visibilidad en metros.                            |
| Sunrise         | Hora de amanecer (formato HH:MM:SS).             |
| Sunset          | Hora de atardecer (formato HH:MM:SS).            |

Es importante destacar que el campo "id" se genera mediante una combinación de las letras de la ciudad y la fecha, lo que garantiza la consistencia de los datos y evita la duplicación de información. Para obtener más detalles sobre cómo utilizar este identificador, consulte el archivo de documentación adjunto.

¡Este proyecto ha sido una experiencia increíblemente enriquecedora y nos ha permitido aprovechar al máximo estas tecnologías modernas! 🌟

