# Camera settings - ESP32-CAM
CAMERA_FRAME_SIZE = "FRAME_SVGA"
if CAMERA_FRAME_SIZE not in [
    "FRAME_96X96",
    "FRAME_QQVGA",
    "FRAME_QCIF",
    "FRAME_HQVGA",
    "FRAME_240X240",
    "FRAME_QVGA",
    "FRAME_CIF",
    "FRAME_HVGA",
    "FRAME_VGA",
    "FRAME_SVGA",
    "FRAME_XGA",
    "FRAME_HD",
    "FRAME_SXGA",
    "FRAME_UXGA",
]:
    raise ValueError("Invalid frame size.")

# 10-63, lower number means higher quality
CAMERA_JPEG_QUALITY = 10
if not (10 <= CAMERA_JPEG_QUALITY <= 63):
    raise ValueError("JPEG quality must be between 10 and 63")

# Camera effects (optional)
CAMERA_FLIP = False  # Flip image upside down
CAMERA_MIRROR = False  # Mirror image left/right
CAMERA_CONTRAST = 0  # -2 to 2
CAMERA_BRIGHTNESS = 0  # -2 to 2
CAMERA_SATURATION = 0  # -2 to 2

CAMERA_AE_LEVELS = 0  # Auto Exposure Level (-2 to 2). Lower is darker.
CAMERA_AGC_GAIN = 0  # Automatic Gain Control (0-30). Lower value is darker.
CAMERA_AEC_VALUE = 100  # Automatic Exposure Control (0-1200). Lower value is darker.

# Validate effect values
for effect, value in [
    ("CAMERA_CONTRAST", CAMERA_CONTRAST),
    ("CAMERA_BRIGHTNESS", CAMERA_BRIGHTNESS),
    ("CAMERA_SATURATION", CAMERA_SATURATION),
]:
    if not -2 <= value <= 2:
        raise ValueError(f"{effect} must be between -2 and 2")

CAMERA_SPECIAL_EFFECT = "EFFECT_NONE"
# Validate special effect
if CAMERA_SPECIAL_EFFECT not in [
    "EFFECT_NONE",
    "EFFECT_NEG",
    "EFFECT_BW",
    "EFFECT_RED",
    "EFFECT_GREEN",
    "EFFECT_BLUE",
    "EFFECT_RETRO",
]:
    raise ValueError("Invalid special effect.")

CAMERA_WHITE_BALANCE = "WB_NONE"

# Validate white balance
if CAMERA_WHITE_BALANCE not in [
    "WB_NONE",
    "WB_SUNNY",
    "WB_CLOUDY",
    "WB_OFFICE",
    "WB_HOME",
]:
    raise ValueError("Invalid white balance.")

# Server settings
PORT = 80
