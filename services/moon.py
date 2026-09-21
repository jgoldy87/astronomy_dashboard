import requests

from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from skyfield.api import load, wgs84
from skyfield import almanac


# Load astronomical ephemeris data
ts = load.timescale()
eph = load("de421.bsp")

earth = eph["earth"]
moon = eph["moon"]


def get_moon_data():
    """Return current astronomical data for the Moon."""

    now = datetime.now(timezone.utc)
    t = ts.from_datetime(now)

    # Moon phase angle
    phase_angle = almanac.moon_phase(eph, t).degrees

    # Percentage illuminated
    illumination = almanac.fraction_illuminated(eph, "moon", t) * 100

    # Distance between Earth and Moon
    astrometric = earth.at(t).observe(moon)
    distance_km = astrometric.distance().km

    # Approximate lunar age
    lunar_age = (phase_angle / 360) * 29.53058867

    phase_name = get_phase_name(phase_angle)

    return {
        "phase": phase_name,
        "phase_angle": phase_angle,
        "illumination": illumination,
        "distance_km": distance_km,
        "lunar_age": lunar_age,
    }


def get_phase_name(angle):
    """Convert lunar phase angle into a familiar phase name."""

    if angle < 22.5 or angle >= 337.5:
        return "New Moon"
    elif angle < 67.5:
        return "Waxing Crescent"
    elif angle < 112.5:
        return "First Quarter"
    elif angle < 157.5:
        return "Waxing Gibbous"
    elif angle < 202.5:
        return "Full Moon"
    elif angle < 247.5:
        return "Waning Gibbous"
    elif angle < 292.5:
        return "Last Quarter"
    else:
        return "Waning Crescent"

def get_upcoming_phases():
    """Return the next four major lunar phase events."""

    now = datetime.now(timezone.utc)

    start_time = ts.from_datetime(now)

    # Search far enough ahead to capture at least four major phases
    end_time = ts.from_datetime(
        now.replace(year=now.year + 1)
    )

    times, phases = almanac.find_discrete(
        start_time,
        end_time,
        almanac.moon_phases(eph),
    )

    phase_names = {
        0: "New Moon",
        1: "First Quarter",
        2: "Full Moon",
        3: "Last Quarter",
    }

    phase_icons = {
        0: "🌑",
        1: "🌓",
        2: "🌕",
        3: "🌗",
    }

    upcoming = []

    for time, phase in zip(times, phases):
        phase_number = int(phase)

        upcoming.append(
            {
                "phase": phase_names[phase_number],
                "icon": phase_icons[phase_number],
                "datetime": time.utc_datetime(),
            }
        )

        if len(upcoming) == 4:
            break

    return upcoming

def get_moon_image():
    """Return NASA's current Dial-A-Moon image."""

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%dT%H:00")

    url = (
        "https://svs.gsfc.nasa.gov/api/dialamoon/"
        f"{timestamp}"
    )

    try:
        response = requests.get(
            url,
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        return {
            "image_url": data["image"]["url"],
            "alt_text": data["image"]["alt_text"],
        }

    except requests.RequestException:
        return None

def azimuth_to_direction(azimuth):
    """Convert azimuth degrees into a compass direction."""

    directions = [
        "North",
        "Northeast",
        "East",
        "Southeast",
        "South",
        "Southwest",
        "West",
        "Northwest",
    ]

    index = round(azimuth / 45) % 8

    return directions[index]

def get_moon_position(latitude, longitude):
    """Return the Moon's current position for an observer."""

    now = datetime.now(timezone.utc)
    t = ts.from_datetime(now)

    observer = earth + wgs84.latlon(
        latitude_degrees=latitude,
        longitude_degrees=longitude,
    )

    apparent = observer.at(t).observe(moon).apparent()

    altitude, azimuth, distance = apparent.altaz()

    return {
        "altitude": altitude.degrees,
        "azimuth": azimuth.degrees,
        "direction": azimuth_to_direction(azimuth.degrees),
        "above_horizon": altitude.degrees > 0,
    }

def get_moonrise_moonset(latitude, longitude, timezone_name):
    """Return the next moonrise and moonset for an observer."""

    local_timezone = ZoneInfo(timezone_name)

    now_utc = datetime.now(timezone.utc)

    start_time = ts.from_datetime(now_utc)
    end_time = ts.from_datetime(
        now_utc + timedelta(days=2)
    )

    observer = wgs84.latlon(
        latitude_degrees=latitude,
        longitude_degrees=longitude,
    )

    moon_up = almanac.risings_and_settings(
        eph,
        moon,
        observer,
    )

    times, events = almanac.find_discrete(
        start_time,
        end_time,
        moon_up,
    )

    moonrise = None
    moonset = None

    for event_time, is_up in zip(times, events):
        event_datetime = (
            event_time.utc_datetime()
            .replace(tzinfo=timezone.utc)
            .astimezone(local_timezone)
        )

        if is_up and moonrise is None:
            moonrise = event_datetime

        elif not is_up and moonset is None:
            moonset = event_datetime

        if moonrise and moonset:
            break

    return {
        "moonrise": moonrise,
        "moonset": moonset,
    }

def get_moon_stats():
    """Return key physical and orbital statistics for the Moon."""

    return {
        "diameter_km": 3474.8,
        "mass_kg": 7.342e22,
        "surface_gravity": 1.62,
        "escape_velocity_kms": 2.38,
        "orbital_period_days": 27.32,
        "rotation_period_days": 27.32,
        "average_distance_km": 384400,
        "surface_area_km2": 37_936_694,
    }