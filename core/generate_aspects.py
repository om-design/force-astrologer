from skyfield.api import load
import json
from datetime import datetime, timezone, timedelta

# Define planets and their Skyfield keys
planet_keys = {
    'Sun': 'sun',
    'Moon': 'moon',
    'Mercury': 'mercury',
    'Venus': 'venus',
    'Mars': 'mars',
    'Jupiter': 'jupiter barycenter',
    'Saturn': 'saturn barycenter',
    'Uranus': 'uranus barycenter',
    'Neptune': 'neptune barycenter',
    'Pluto': 'pluto barycenter'
}

aspect_angles = {
    'Conjunction': 0,
    'Sextile': 60,
    'Square': 90,
    'Trine': 120,
    'Opposition': 180
}
aspect_orbs = {
    'Conjunction': 8,
    'Sextile': 4,
    'Square': 6,
    'Trine': 6,
    'Opposition': 8
}

def get_positions_and_speeds(t, eph, planet_keys):
    positions = {}
    speeds = {}
    for name, key in planet_keys.items():
        planet = eph[key]
        astrometric = eph['earth'].at(t).observe(planet)
        ra, dec, distance = astrometric.ecliptic_latlon()
        positions[name] = ra.degrees % 360
        # Calculate speed (deg/day) by comparing to position 1 day later
        t_later = t + 1
        astrometric_later = eph['earth'].at(t_later).observe(planet)
        ra_later, _, _ = astrometric_later.ecliptic_latlon()
        pos_later = ra_later.degrees % 360
        speed = (pos_later - positions[name]) % 360
        if speed > 180: speed -= 360
        speeds[name] = speed
    return positions, speeds

def get_aspects():
    ts = load.timescale()
    now = datetime.now(timezone.utc)
    t = ts.utc(now.year, now.month, now.day, now.hour, now.minute)
    eph = load('de421.bsp')
    positions, speeds = get_positions_and_speeds(t, eph, planet_keys)
    aspects = []
    planet_names = list(planet_keys.keys())
    for i, p1 in enumerate(planet_names):
        for j, p2 in enumerate(planet_names):
            if j <= i: continue
            angle = abs(positions[p1] - positions[p2])
            angle = angle if angle <= 180 else 360 - angle
            for aspect, aspect_angle in aspect_angles.items():
                if abs(angle - aspect_angle) <= aspect_orbs[aspect]:
                    # Calculate time left in aspect
                    orb = aspect_orbs[aspect]
                    rel_speed = abs(speeds[p1] - speeds[p2])
                    if rel_speed == 0:
                        time_left_days = 99  # arbitrarily long
                    else:
                        time_left_days = (orb - abs(angle - aspect_angle)) / abs(rel_speed)
                    end_time = now + timedelta(days=max(0.1, time_left_days))
                    aspects.append({
                        "planet1": p1,
                        "planet2": p2,
                        "aspect": aspect,
                        "start": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "end": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "angle": round(angle, 2)
                    })
    return aspects

if __name__ == "__main__":
    aspects = get_aspects()
    with open('current_aspects.json', 'w') as f:
        json.dump(aspects, f, indent=2)
    print("Wrote current_aspects.json with", len(aspects), "aspects.")
