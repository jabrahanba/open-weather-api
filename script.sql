CREATE TABLE jabrahanba_coderhouse.weather_data (
    id VARCHAR(15),
    date DATE,
    country VARCHAR(15),
    capital VARCHAR(50),
    temperature NUMERIC(5, 2),
    feels_like NUMERIC(5, 2),
    pressure INT,
    humidity INT,
    weather VARCHAR(50),
    description VARCHAR(50),
    wind_speed NUMERIC(5, 2),
    wind_direction INT,
    cloudiness INT,
    visibility INT,
    sunrise TIMESTAMP,
    sunset TIMESTAMP
);