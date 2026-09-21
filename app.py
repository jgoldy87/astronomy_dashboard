import streamlit as st

from services.moon import (
    get_moon_data,
    get_upcoming_phases,
    get_moon_image,
    get_moon_position,
    get_moonrise_moonset,
)


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

st.header("🌙 The Moon")

moon_image = get_moon_image()

left, center, right = st.columns([1, 2, 1])

with center:
    st.image(
        moon_image["image_url"],
        caption="Current Moon — NASA Goddard",
        use_container_width=True,
    )

moon = get_moon_data()

moon_position = get_moon_position(
    latitude,
    longitude,
)

moon_events = get_moonrise_moonset(
    latitude,
    longitude,
    timezone_name,
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Phase",
        moon["phase"],
    )

with col2:
    st.metric(
        "Illumination",
        f'{moon["illumination"]:.1f}%',
    )

with col3:
    st.metric(
        "Distance from Earth",
        f'{moon["distance_km"]:,.0f} km',
    )

with col4:
    st.metric(
        "Lunar Age",
        f'{moon["lunar_age"]:.1f} days',
    )

def format_event_time(event):
    if event is None:
        return "N/A"

    return event.strftime("%I:%M %p").lstrip("0")

st.divider()

st.subheader("🌙 Moon in the Sky")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Next Moonrise",
        format_event_time(
            moon_events["moonrise"]
        ),
    )

with col2:
    st.metric(
        "Next Moonset",
        format_event_time(
            moon_events["moonset"]
        ),
    )

with col3:
    st.metric(
        "Altitude",
        f'{moon_position["altitude"]:.1f}°',
    )

with col4:
    st.metric(
        "Azimuth",
        f'{moon_position["azimuth"]:.1f}°',
    )

with col5:
    st.metric(
        "Direction",
        moon_position["direction"],
    )

if moon_position["above_horizon"]:
    st.success(
        "🌙 The Moon is currently above the horizon."
    )
else:
    st.info(
        "🌙 The Moon is currently below the horizon."
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