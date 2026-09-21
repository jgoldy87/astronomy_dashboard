import streamlit as st

from services.moon import (
    get_moon_data,
    get_upcoming_phases,
    get_moon_image,
    get_moon_position,
    get_moonrise_moonset,
    get_moon_stats,
)

from data.lunar_locations import LUNAR_LOCATIONS

from services.moon_map import create_location_map

@st.cache_data(ttl=3600)
def load_moon_image():
    image = get_moon_image()

    if image is None:
        raise RuntimeError(
            "NASA Moon image temporarily unavailable."
        )

    return image

st.set_page_config(
    page_title="Astronomy Dashboard",
    page_icon="🌌",
    layout="wide",
)

st.title("🌌 Astronomy Dashboard")
st.caption("Exploring the universe through data")

st.sidebar.header("Observer Location")

st.sidebar.caption(
    "Enter the coordinates for your observing location."
)

latitude = st.sidebar.number_input(
    "Latitude",
    min_value=-90.0,
    max_value=90.0,
    value=42.6526,
    format="%.4f",
)

longitude = st.sidebar.number_input(
    "Longitude",
    min_value=-180.0,
    max_value=180.0,
    value=-73.7562,
    format="%.4f",
)

timezone_name = st.sidebar.text_input(
    "Timezone",
    value="America/New_York",
    help="Use an IANA timezone such as America/New_York, Europe/London, or Asia/Tokyo.",
)

st.sidebar.link_button(
    "📍 Find My Coordinates",
    "https://www.latlong.net/",
)

st.title("🌙 The Moon")

st.caption(
    "Earth's natural satellite — current conditions, "
    "observation data, and lunar exploration."
)

st.divider()

moon = get_moon_data()
try:
    moon_image = load_moon_image()
except RuntimeError:
    moon_image = None
moon_stats = get_moon_stats()

moon_position = get_moon_position(
    latitude,
    longitude,
)

moon_events = get_moonrise_moonset(
    latitude,
    longitude,
    timezone_name,
)

image_col, data_col = st.columns(
    [1.2, 1],
    gap="large",
)

with image_col:
    if moon_image:
        st.image(
            moon_image["image_url"],
            use_container_width=True,
        )

        st.caption(
            "Current Moon visualization — NASA Goddard"
        )

    else:
        st.info(
            "NASA's current Moon visualization "
            "is temporarily unavailable."
        )

with data_col:
    st.subheader("Current Moon")

    st.markdown(
        f"## {moon['phase']}"
    )

    st.caption(
        "Current lunar phase"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Illumination",
            f'{moon["illumination"]:.1f}%',
        )

    with col2:
        st.metric(
            "Lunar Age",
            f'{moon["lunar_age"]:.1f} days',
        )

    st.metric(
        "Distance from Earth",
        f'{moon["distance_km"]:,.0f} km',
    )

    st.caption(
        "Lunar age measures the number of days "
        "since the most recent New Moon."
    )

def format_event_time(event):
    if event is None:
        return "N/A"

    return event.strftime("%I:%M %p").lstrip("0")

st.divider()

st.subheader("🌙 Moon in the Sky")

st.caption(
    "Current observing conditions for your selected location."
)

status_col, position_col = st.columns(
    [1, 1.5],
    gap="large",
)

# Moonrise and moonset
with status_col:
    st.markdown("#### Visibility")

    if moon_position["above_horizon"]:
        st.success(
            "🌙 The Moon is currently above the horizon."
        )
    else:
        st.info(
            "🌙 The Moon is currently below the horizon."
        )

    rise_col, set_col = st.columns(2)

    with rise_col:
        st.metric(
            "Next Moonrise",
            format_event_time(
                moon_events["moonrise"]
            ),
        )

    with set_col:
        st.metric(
            "Next Moonset",
            format_event_time(
                moon_events["moonset"]
            ),
        )

# Current sky position
with position_col:
    st.markdown("#### Current Position")

    altitude_col, azimuth_col, direction_col = st.columns(3)

    with altitude_col:
        st.metric(
            "Altitude",
            f'{moon_position["altitude"]:.1f}°',
        )

    with azimuth_col:
        st.metric(
            "Azimuth",
            f'{moon_position["azimuth"]:.1f}°',
        )

    with direction_col:
        st.metric(
            "Direction",
            moon_position["direction"],
        )

    st.caption(
        "Altitude measures how high the Moon is above or "
        "below the horizon. Azimuth gives its compass "
        "direction, measured clockwise from north."
    )

st.divider()

st.subheader("Upcoming Lunar Phases")

upcoming_phases = get_upcoming_phases()

cols = st.columns(4)

for col, phase in zip(cols, upcoming_phases):
    with col:
        st.markdown(
            f"### {phase['icon']} {phase['phase']}"
        )

        st.write(
            phase["datetime"].strftime("%B %d, %Y")
        )

st.divider()

st.subheader("📊 Moon Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Diameter",
        f'{moon_stats["diameter_km"]:,.1f} km',
    )

with col2:
    st.metric(
        "Surface Gravity",
        f'{moon_stats["surface_gravity"]:.2f} m/s²',
    )

with col3:
    st.metric(
        "Escape Velocity",
        f'{moon_stats["escape_velocity_kms"]:.2f} km/s',
    )

with col4:
    st.metric(
        "Average Distance",
        f'{moon_stats["average_distance_km"]:,.0f} km',
    )

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Mass",
        f'{moon_stats["mass_kg"]:.3e} kg',
    )

with col2:
    st.metric(
        "Orbital Period",
        f'{moon_stats["orbital_period_days"]:.2f} days',
    )

with col3:
    st.metric(
        "Rotation Period",
        f'{moon_stats["rotation_period_days"]:.2f} days',
    )

with col4:
    st.metric(
        "Surface Area",
        f'{moon_stats["surface_area_km2"]:,.0f} km²',
    )

st.caption(
    "The Moon's surface gravity is about 16.5% of Earth's. "
    "A 180 lb person would weigh about 30 lb on the Moon."
)

st.divider()

st.subheader("🔭 Explore the Moon")

st.write(
    "Explore famous craters, lunar maria, and historic "
    "landing sites on the Moon."
)

selected_location = st.selectbox(
    "Choose a lunar location",
    LUNAR_LOCATIONS.keys(),
)

location = LUNAR_LOCATIONS[selected_location]

location_map = create_location_map(
    location["latitude"],
    location["longitude"],
)

if "image" in location:

    image_col, info_col, map_col = st.columns(
        [1.4, 0.9, 1.2]
    )

    # Detailed NASA image
    with image_col:
        st.image(
            location["image"],
            use_container_width=True,
        )

        st.caption(
            location["image_credit"]
        )

    # Location information
    with info_col:
        st.markdown(
            f"### {selected_location}"
        )

        st.write(
            f'**Type**  \n{location["type"]}'
        )

        st.write(
            f'**Region**  \n{location["region"]}'
        )

        latitude_direction = (
            "N"
            if location["latitude"] >= 0
            else "S"
        )

        longitude_direction = (
            "E"
            if location["longitude"] >= 0
            else "W"
        )

        st.write(
            f'**Latitude**  \n'
            f'{abs(location["latitude"]):.2f}° '
            f'{latitude_direction}'
        )

        st.write(
            f'**Longitude**  \n'
            f'{abs(location["longitude"]):.2f}° '
            f'{longitude_direction}'
        )

        st.write(
            location["description"]
        )

    # Location map
    with map_col:
        st.markdown(
            "### Location on the Moon"
        )

        st.image(
            location_map,
            use_container_width=True,
        )

        if location["type"] == "Lunar Mare":
            map_caption = (
                f"The red square indicates the approximate "
                f"region of {selected_location}."
            )
        else:
            map_caption = (
                f"The red square shows the approximate "
                f"location of {selected_location}."
            )

        st.caption(map_caption)

