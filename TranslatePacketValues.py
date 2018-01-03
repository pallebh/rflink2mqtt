from typing import Any, Callable, Dict, Generator, cast

PACKET_FIELDS = {
    'awinsp': 'average_windspeed',
    'baro': 'barometric_pressure',
    'bat': 'battery',
    'bforecast': 'weather_forecast',
    'chime': 'doorbell_melody',
    'cmd': 'command',
    'co2': 'co2_air_quality',
    'current': 'current_phase_1',
    'current2': 'current_phase_2',
    'current3': 'current_phase_3',
    'dist': 'distance',
    'fw': 'firmware',
    'hstatus': 'humidity_status',
    'hum': 'humidity',
    'hw': 'hardware',
    'kwatt': 'kilowatt',
    'lux': 'light_intensity',
    'meter': 'meter_value',
    'rain': 'total_rain',
    'rainrate': 'rain_rate',
    'raintot': 'total_rain',
    'rev': 'revision',
    'sound': 'noise_level',
    'temp': 'temperature',
    'uv': 'uv_intensity',
    'ver': 'version',
    'volt': 'voltage',
    'watt': 'watt',
    'winchl': 'windchill',
    'windir': 'winddirection',
    'wings': 'windgusts',
    'winsp': 'windspeed',
    'wintmp': 'windtemp',
}

UNITS = {
    'awinsp': 'km/h',
    # depends on sensor
    'baro': None,
    'bat': None,
    'bforecast': None,
    'chime': None,
    'cmd': None,
    'co2': None,
    'current': 'A',
    'current2': 'A',
    'current3': 'A',
    # depends on sensor
    'dist': None,
    'fw': None,
    'hstatus': None,
    'hum': '%',
    'hw': None,
    'kwatt': 'kW',
    'lux': 'lux',
    # depends on sensor
    'meter': None,
    'rain': 'mm',
    'rainrate': 'mm',
    'raintot': 'mm',
    'rev': None,
    # unknown, might be dB?
    'sound': None,
    # might be °F, but default to something
    'temp': '°C',
    'uv': None,
    'ver': None,
    'volt': 'v',
    'watt': 'w',
    'winchl': '°C',
    'windir': '°',
    'wings': 'km/h',
    'winsp': 'km/h',
    'wintmp': '°C',
}

HSTATUS_LOOKUP = {
    '0': 'normal',
    '1': 'comfortable',
    '2': 'dry',
    '3': 'wet',
}
BFORECAST_LOOKUP = {
    '0': 'no_info',
    '1': 'sunny',
    '2': 'partly_cloudy',
    '3': 'cloudy',
    '4': 'rain',
}


def signed_to_float(hex: str) -> float:
    """Convert signed hexadecimal to floating value."""
    if int(hex, 16) & 0x8000:
        return -(int(hex, 16) & 0x7FFF) / 10
    else:
        return int(hex, 16) / 10


keyword2function = {
    'awinsp': lambda hex: int(hex, 16) / 10,
    'baro': lambda hex: int(hex, 16),
    'bforecast': lambda x: BFORECAST_LOOKUP.get(x, 'Unknown'),
    'chime': lambda hex: int(hex, 16),
    'co2': int,
    'current': int,
    'current2': int,
    'current3': int,
    'dist': int,
    'hstatus': lambda x: HSTATUS_LOOKUP.get(x, 'Unknown'),
    'hum': int,
    'kwatt': lambda hex: int(hex, 16),
    'lux': lambda hex: int(hex, 16),
    'meter': int,
    'rain': lambda hex: int(hex, 16) / 10,
    'rainrate': lambda hex: int(hex, 16) / 10,
    'raintot': lambda hex: int(hex, 16) / 10,
    'sound': int,
    'temp': signed_to_float,
    'uv': lambda hex: int(hex, 16),
    'volt': int,
    'watt': lambda hex: int(hex, 16),
    'winchl': signed_to_float,
    'windir': lambda windir: int(windir) * 22.5,
    'wings': lambda hex: int(hex, 16) / 10,
    'winsp': lambda hex: int(hex, 16) / 10,
    'wintmp': signed_to_float,
    'id':lambda hex: int(hex, 16)
}

def translates( keyword , value ):
    k2f =keyword2function
    units = UNITS

    func = lambda x: x
    if keyword in k2f :
        func = k2f[ keyword ]

    if not func and keyword in units :
        func = units[keyword]

    return func( value )
