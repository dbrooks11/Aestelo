from geopy.distance import distance

def average_location(coords):
    if not coords:
        return None
    
    avg_lat = sum(c['lat'] for c in coords) / len(coords)
    avg_long = sum(c['long'] for c in coords) / len(coords)

    threshold_meters = 30
    filtered = [
        c for c in coords
        if distance((c['lat'], c['long']), (avg_lat, avg_long)).m <= threshold_meters
    ]

    if not filtered:
        return None 

    avg_lat = sum(c['lat'] for c in filtered) / len(filtered)
    avg_long = sum(c['long'] for c in filtered) / len(filtered)

    alts = [c['alt'] for c in filtered if c.get('alt') is not None]
    avg_alt = sum(alts) / len(alts) if alts else None

    return {'lat': avg_lat, 'long': avg_long, 'alt': avg_alt}
