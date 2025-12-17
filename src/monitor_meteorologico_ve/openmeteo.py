from abc import ABC, abstractmethod
from datetime import datetime
import os

from dotenv import load_dotenv

import requests

load_dotenv()


class OpenMeteoAPIClient:
    """
    Clase para interactuar con la API de OpenMeteoAPIClient
    """

    def __init__(self):
        """
        Constructor de la clase OpenMeteoAPIClient

        Inicializa la url base para las peticiones a la API de OpenMeteo
        """
        self.url_base = "https://api.open-meteo.com/v1/forecast"
        self.url_historical_base = "https://archive-api.open-meteo.com/v1/archive"

    def get_historical_data(
        self,
        lat,
        lon,
        start_date,
        end_date,
        daily="temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum",
    ):
        """
        Obtiene los datos climáticos historicos de una ubicación

        Args:
            lat (float): Latitud de la ubicación
            lon (float): Longitud de la ubicación
            start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'
            end_date (str): Fecha de fin en formato 'YYYY-MM-DD'
            daily (str, optional): Campos de datos climáticos diarios separados por comas. Por defecto, 'temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum'

        Returns:
            dict: Diccionario con los datos climáticos historicos
        """
        if end_date > datetime.now().strftime("%Y-%m-%d"):
            end_date = datetime.now().strftime("%Y-%m-%d")
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": daily,
            "timezone": "auto",
        }
        try:
            response = requests.get(self.url_historical_base, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                print("Error en la solicitud de datos climáticos.")
            if e.response.status_code == 404:
                print(
                    "No se encontraron datos climáticos para la ubicación especificada."
                )
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de Open-Meteo: {e}")

        return response.json()


class WeatherAPI:
    """
    Clase para interactuar con la API de WetherAPI
    """

    def __init__(self):
        """
        Constructor de la clase WeatherAPI

        Inicializa la url base para las peticiones a la API de WeatherAPI
        """
        self.url_base = "http://api.weatherapi.com/v1"
        self.url_historical_base = "http://api.weatherapi.com/v1/history.json"
        self.api_key = os.getenv("WEATHER_API_KEY")

    def get_historical_data(
        self,
        lat,
        lon,
        start_date,
        end_date,
    ):
        """
        Obtiene los datos climáticos historicos de una ubicación

        Args:
            lat (float): Latitud de la ubicación
            lon (float): Longitud de la ubicación
            start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'
            end_date (str): Fecha de fin en formato 'YYYY-MM-DD'
            daily (str, optional): Campos de datos climáticos diarios separados por comas. Por defecto, 'temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum'

        Returns:
            dict: Diccionario con los datos climáticos historicos
        """
        if end_date > datetime.now().strftime("%Y-%m-%d"):
            end_date = datetime.now().strftime("%Y-%m-%d")

        if start_date < "2010-01-01":
            start_date = "2010-01-01"

        params = {
            "q": f"{lat},{lon}",  # Utiliza la ubicación en formato "lat,lon"
            "dt": start_date,
            "end_dt": end_date,
            "key": self.api_key,
        }
        try:
            response = requests.get(self.url_historical_base, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                print("Error en la solicitud de datos climáticos.")
            if e.response.status_code == 404:
                print(
                    "No se encontraron datos climáticos para la ubicación especificada."
                )
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de Open-Meteo: {e}")

        return response


if __name__ == "__main__":
    api_client = WeatherAPI()
    lat = 8.80
    lon = -70.86
    start_date = "2025-06-20"
    end_date = "2025-06-30"
    data = api_client.get_historical_data(lat, lon, start_date, end_date)
    print(data)

# if __name__ == "__main__":
#     api_client = OpenMeteoAPIClient()
#     lat = 8.80
#     lon = -70.86
#     start_date = "2025-06-20"
#     end_date = "2025-06-30"
#     data = api_client.get_historical_data(lat, lon, start_date, end_date)
#     print(data)
