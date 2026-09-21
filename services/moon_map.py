from PIL import Image, ImageDraw


MOON_MAP_PATH = "data/images/moon_nearside.jpg"


def lunar_coordinates_to_pixels(
    latitude,
    longitude,
    width,
    height,
):
    """
    Convert lunar latitude/longitude to approximate pixel
    coordinates on an orthographic near-side Moon image.
    """

    import math

    lat = math.radians(latitude)
    lon = math.radians(longitude)

    x = math.cos(lat) * math.sin(lon)
    y = math.sin(lat)

    pixel_x = (width / 2) + (x * width / 2)
    pixel_y = (height / 2) - (y * height / 2)

    return int(pixel_x), int(pixel_y)


def create_location_map(latitude, longitude):
    """Draw a red square around a location on the Moon."""

    image = Image.open(MOON_MAP_PATH).convert("RGB")

    width, height = image.size

    x, y = lunar_coordinates_to_pixels(
        latitude,
        longitude,
        width,
        height,
    )

    draw = ImageDraw.Draw(image)

    box_size = max(12, int(width * 0.035))

    draw.rectangle(
        [
            x - box_size,
            y - box_size,
            x + box_size,
            y + box_size,
        ],
        outline="red",
        width=max(3, int(width * 0.006)),
    )

    return image