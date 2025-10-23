from geopy.distance import distance

def average_location(coords):
    if not coords:
        return None
    
    avg_lat = sum(c['latitude'] for c in coords) / len(coords)
    avg_long = sum(c['longitude'] for c in coords) / len(coords)

    threshold_meters = 30
    filtered = [
        c for c in coords
        if distance((c['latitude'], c['longitude']), (avg_lat, avg_long)).m <= threshold_meters
    ]

    if not filtered:
        return None 

    avg_lat = sum(c['latitude'] for c in filtered) / len(filtered)
    avg_long = sum(c['longitude'] for c in filtered) / len(filtered)

    alts = [c['altitude'] for c in filtered if c.get('altitude') is not None]
    avg_alt = sum(alts) / len(alts) if alts else None

    return {'latitude': avg_lat, 'longitude': avg_long, 'altitude': avg_alt}
