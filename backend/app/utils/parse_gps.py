from typing import cast
from geopy.distance import geodesic



class GPSHandling:
    LOCATION_KEY_LAT = 'lat'
    LOCATION_KEY_LON = 'long'

    async def parse_gps_data_pyvips(self, exif: dict[str, str]) -> dict[str, str | list[str]] | None:
        exif_parse = {} 
        tag = 'GPS'
        for field, value in exif:
            if tag in field:
                if not value:
                    return None
                parse: str = value.split('(')[1].strip(')')
                if parse[0] in ['N','S','E','W']:
                    parsed_direction: str = parse[0]   
                else:
                    parsed_data: list[str] = parse.split(',', maxsplit=3)[:3]
                exif_parse[field.split(tag)[1].lower()] = parsed_direction or parsed_data

        return exif_parse


    async def get_lat_long(self, exif: dict[str, str] | None) -> dict[str, float] | None:
        if not exif:
            return None
        
        parsed_gps_data = await self.parse_gps_data_pyvips(exif=exif)

        if not parsed_gps_data:
            return None
        
        parsed_gps_data = cast(dict, parsed_gps_data)
        lat_ref: str = parsed_gps_data.get('latituderef')       # type: ignore[attr-defined]
        lat_d,lat_m,lat_s = parsed_gps_data.get('latitude')         # type: ignore

        long_ref: str = parsed_gps_data('longituderef')     # type: ignore[attr-defined]
        long_d,long_m,long_s = parsed_gps_data('longitude')     # type: ignore

        async def dms_to_decimal(ref: str, decimal: str, minute: str, second: str) -> float | None:
            decimal_result: float = float(decimal) + (float(minute) / 60) + (float(second) /3600)
            if not decimal_result:
                return None
            
            if ref in ['S', 'W']:
                decimal_result = -decimal_result

            return float(f'{decimal_result:.6f}')
        
        return {self.LOCATION_KEY_LAT: await dms_to_decimal(ref=lat_ref, decimal=lat_d, minute=lat_m, second=lat_s),
                self.LOCATION_KEY_LON: await dms_to_decimal(ref=long_ref, decimal=long_d, minute=long_m, second=long_s)}  # type: ignore
    
    from geopy.distance import geodesic



    async def average_location(self, coords: list[dict[str, float]]) -> dict | None:
        if not coords:
            return None

        avg_lat = sum(c[self.LOCATION_KEY_LAT] for c in coords) / len(coords)
        avg_lon = sum(c[self.LOCATION_KEY_LON] for c in coords) / len(coords)

        threshold_meters = 200  
        filtered = [c for c in coords
            if geodesic(
                (c[self.LOCATION_KEY_LAT], c[self.LOCATION_KEY_LON]),
                (avg_lat, avg_lon)
            ).meters <= threshold_meters]

        if not filtered or (len(filtered) != len(coords)):
            return None

        avg_lat = sum(c[self.LOCATION_KEY_LAT] for c in filtered) / len(filtered)
        avg_lon = sum(c[self.LOCATION_KEY_LON] for c in filtered) / len(filtered)

        return {self.LOCATION_KEY_LAT: avg_lat, self.LOCATION_KEY_LON: avg_lon}

gps = GPSHandling()