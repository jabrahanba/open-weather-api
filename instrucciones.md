# Instrucciones de Uso del Proyecto ETL con Airflow y Amazon Redshift 🚀

✅ 1. *Clonar el Repositorio:* Primero, clona este repositorio en tu máquina local.

✅ 2. *Verificar Dependencias:* Asegúrate de tener Docker y Python instalados en tu equipo.

✅ 3. *Ejecutar Docker Compose:* Ejecuta el siguiente comando para levantar los servicios necesarios:

   ```bash
   docker-compose up -d

Esto iniciará los contenedores necesarios para la aplicación.

✅ 4. *Accede a la UI de Airflow:* Abre tu navegador web y navega a la interfaz de usuario de Airflow. La URL por defecto es http://localhost:8080.

✅ 5. *Inicia Sesión en Airflow:* Utiliza las siguientes credenciales para iniciar sesión:

Usuario: admin
Contraseña: (Sigue las instrucciones a continuación para obtenerla).
Obtener la Contraseña de Airflow: Utiliza el siguiente comando para obtener la contraseña de Airflow desde el contenedor del servicio web:
 

   ```bash
   docker exec -it [ID_DEL_CONTENEDOR_DEL_WEBSERVICE] cat standalone_admin_password.txt

📝Reemplaza [ID_DEL_CONTENEDOR_DEL_WEBSERVICE] con el ID del contenedor del servicio web.

✅ 6. *Configurar Variables en Airflow:* Una vez iniciada la sesión en la UI de Airflow, ve a la sección "Admin" y selecciona "Variables". Carga el archivo con las credenciales necesarias para ejecutar el DAG.

¡Listo para Utilizar! Ahora, la aplicación está lista para su uso. Puedes ejecutar el DAG para obtener los datos meteorológicos de las principales ciudades de Sudamérica y realizar análisis u otras operaciones con ellos.

¡Disfruta explorando y utilizando esta aplicación para automatizar tus procesos de ETL y obtener datos actualizados del clima! Si tienes alguna pregunta o necesitas asistencia adicional, no dudes en contactarnos.

¡Feliz análisis de datos! 🌦️📊