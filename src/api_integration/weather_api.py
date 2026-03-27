import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time

class EnhancedWeatherAPI:
    """
    Sarkaari-grade Weather API Integration System
    Multiple API failover, agricultural metrics, and bureaucratic precision
    """
    
    def __init__(self):
        self.apis = {
            'openweathermap': {
                'base_url': 'https://api.openweathermap.org/data/2.5',
                'forecast_url': 'https://api.openweathermap.org/data/2.5/forecast',
                'key_required': True
            },
            'weatherapi': {
                'base_url': 'https://api.weatherapi.com/v1',
                'forecast_url': 'https://api.weatherapi.com/v1/forecast.json',
                'key_required': True
            },
            'accuweather': {
                'base_url': 'http://dataservice.accuweather.com',
                'key_required': True
            }
        }
        
        self.cache = {}
        self.cache_duration = 1800  # 30 minutes cache for sarkaari efficiency
        
    def _get_cache_key(self, api_name: str, city: str, endpoint: str) -> str:
        """Generate bureaucratic cache key"""
        return f"{api_name}_{city}_{endpoint}_{datetime.now().hour}"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid as per government regulations"""
        if cache_key not in self.cache:
            return False
        cached_time = self.cache[cache_key]['timestamp']
        return (time.time() - cached_time) < self.cache_duration
    
    def _calculate_agricultural_metrics(self, weather_data: Dict) -> Dict:
        """
        Calculate agricultural metrics based on weather data
        Following ICAR guidelines for precision farming
        """
        temp = weather_data.get('main', {}).get('temp', 25)
        humidity = weather_data.get('main', {}).get('humidity', 60)
        wind_speed = weather_data.get('wind', {}).get('speed', 2)
        rain_prob = weather_data.get('rain', {}).get('1h', 0)
        
        # Evapotranspiration calculation (simplified Hargreaves method)
        et = 0.0023 * (temp + 17.8) * (temp - 20) ** 0.5 * (1 - humidity/100)
        
        # Irrigation recommendation
        irrigation_need = "LOW"
        if temp > 35 and humidity < 40:
            irrigation_need = "HIGH"
        elif temp > 30 or humidity < 50:
            irrigation_need = "MEDIUM"
        
        # Soil moisture estimation
        soil_moisture = max(0, min(100, (100 - temp) + humidity - rain_prob * 10))
        
        return {
            'evapotranspiration': round(et, 2),
            'irrigation_need': irrigation_need,
            'soil_moisture_estimated': round(soil_moisture, 1),
            'heat_stress_index': "HIGH" if temp > 38 else "MEDIUM" if temp > 32 else "LOW",
            'disease_risk': "HIGH" if humidity > 80 and temp > 25 else "MEDIUM" if humidity > 60 else "LOW"
        }
    
    def get_openweather_data(self, api_key: str, city: str) -> Optional[Dict]:
        """OpenWeatherMap API with agricultural enhancements"""
        cache_key = self._get_cache_key('openweathermap', city, 'current')
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        url = f"{self.apis['openweathermap']['base_url']}/weather"
        params = {
            'appid': api_key,
            'q': city,
            'units': 'metric',
            'lang': 'en'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                data['agricultural_metrics'] = self._calculate_agricultural_metrics(data)
                data['source'] = 'OpenWeatherMap'
                data['official_timestamp'] = datetime.now().isoformat()
                
                self.cache[cache_key] = {
                    'data': data,
                    'timestamp': time.time()
                }
                return data
        except Exception as e:
            print(f"OpenWeatherMap API Error: {e}")
        return None
    
    def get_weatherapi_data(self, api_key: str, city: str) -> Optional[Dict]:
        """WeatherAPI.com with agricultural focus"""
        cache_key = self._get_cache_key('weatherapi', city, 'current')
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        url = f"{self.apis['weatherapi']['forecast_url']}"
        params = {
            'key': api_key,
            'q': city,
            'aqi': 'no',
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Convert to standard format
                standardized = {
                    'main': {
                        'temp': data['current']['temp_c'],
                        'humidity': data['current']['humidity'],
                        'pressure': data['current']['pressure_mb']
                    },
                    'wind': {
                        'speed': data['current']['wind_kph'] / 3.6,  # Convert to m/s
                        'deg': data['current']['wind_degree']
                    },
                    'weather': [{
                        'main': data['current']['condition']['text'],
                        'description': data['current']['condition']['text']
                    }],
                    'location': data['location'],
                    'source': 'WeatherAPI',
                    'official_timestamp': datetime.now().isoformat()
                }
                
                standardized['agricultural_metrics'] = self._calculate_agricultural_metrics(standardized)
                
                self.cache[cache_key] = {
                    'data': standardized,
                    'timestamp': time.time()
                }
                return standardized
        except Exception as e:
            print(f"WeatherAPI Error: {e}")
        return None
    
    def get_forecast(self, api_key: str, city: str, days: int = 5) -> List[Dict]:
        """Get extended forecast for agricultural planning"""
        forecasts = []
        
        # Try OpenWeatherMap first
        try:
            url = f"{self.apis['openweathermap']['forecast_url']}"
            params = {
                'appid': api_key,
                'q': city,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data['list'][:days * 8]:
                    forecast = {
                        'datetime': item['dt_txt'],
                        'temp': item['main']['temp'],
                        'humidity': item['main']['humidity'],
                        'weather': item['weather'][0]['main'],
                        'rain': item.get('rain', {}).get('3h', 0),
                        'agricultural_metrics': self._calculate_agricultural_metrics(item)
                    }
                    forecasts.append(forecast)
        except Exception as e:
            print(f"Forecast API Error: {e}")
        
        return forecasts
    
    def get_weather_alerts(self, api_key: str, city: str) -> List[Dict]:
        """Get agricultural weather alerts and warnings"""
        alerts = []
        
        # This would require premium APIs for real alerts
        # For now, we'll generate based on current conditions
        current = self.get_openweather_data(api_key, city)
        
        if current:
            temp = current['main']['temp']
            humidity = current['main']['humidity']
            weather = current['weather'][0]['main'].lower()
            
            if temp > 40:
                alerts.append({
                    'type': 'EXTREME_HEAT',
                    'severity': 'HIGH',
                    'message': f'Extreme heat warning: {temp}°C. Increase irrigation frequency.',
                    'action_required': 'Increase irrigation by 30%'
                })
            
            if 'rain' in weather and humidity > 85:
                alerts.append({
                    'type': 'FUNGAL_DISEASE_RISK',
                    'severity': 'MEDIUM',
                    'message': 'High humidity and rain conditions increase fungal disease risk.',
                    'action_required': 'Monitor crops for signs of infection'
                })
            
            if temp < 10:
                alerts.append({
                    'type': 'FROST_WARNING',
                    'severity': 'HIGH',
                    'message': f'Low temperature alert: {temp}°C. Risk of frost damage.',
                    'action_required': 'Consider frost protection measures'
                })
        
        return alerts
    
    def get_comprehensive_weather(self, api_keys: Dict[str, str], city: str) -> Dict:
        """
        Master weather function with API failover
        Sarkaari redundancy protocol activated
        """
        results = {
            'primary': None,
            'backup': None,
            'forecasts': [],
            'alerts': [],
            'agricultural_summary': {},
            'api_status': {},
            'last_updated': datetime.now().isoformat()
        }
        
        # Try primary API (OpenWeatherMap)
        if api_keys.get('openweathermap'):
            results['primary'] = self.get_openweather_data(api_keys['openweathermap'], city)
            results['api_status']['openweathermap'] = 'SUCCESS' if results['primary'] else 'FAILED'
        
        # Try backup API (WeatherAPI)
        if not results['primary'] and api_keys.get('weatherapi'):
            results['backup'] = self.get_weatherapi_data(api_keys['weatherapi'], city)
            results['api_status']['weatherapi'] = 'SUCCESS' if results['backup'] else 'FAILED'
        
        # Use whichever worked
        working_data = results['primary'] or results['backup']
        
        if working_data:
            # Get forecasts
            if api_keys.get('openweathermap'):
                results['forecasts'] = self.get_forecast(api_keys['openweathermap'], city)
            
            # Get alerts
            results['alerts'] = self.get_weather_alerts(api_keys.get('openweathermap', ''), city)
            
            # Generate agricultural summary
            metrics = working_data.get('agricultural_metrics', {})
            results['agricultural_summary'] = {
                'overall_irrigation_recommendation': metrics.get('irrigation_need', 'MEDIUM'),
                'evapotranspiration_rate': metrics.get('evapotranspiration', 0),
                'soil_moisture_status': metrics.get('soil_moisture_estimated', 50),
                'crop_stress_level': metrics.get('heat_stress_index', 'LOW'),
                'disease_outbreak_risk': metrics.get('disease_risk', 'LOW'),
                'government_advisory': self._generate_government_advisory(metrics)
            }
        
        return results
    
    def _generate_government_advisory(self, metrics: Dict) -> str:
        """Generate official government advisory message"""
        advisories = []
        
        if metrics.get('irrigation_need') == 'HIGH':
            advisories.append("Immediate irrigation recommended as per Ministry of Agriculture guidelines")
        elif metrics.get('heat_stress_index') == 'HIGH':
            advisories.append("Heat stress conditions detected. Provide shade and additional water")
        elif metrics.get('disease_risk') == 'HIGH':
            advisories.append("High disease risk reported. Contact agricultural officer for preventive measures")
        
        if not advisories:
            advisories.append("Normal conditions. Continue standard irrigation practices")
        
        return " | ".join(advisories)