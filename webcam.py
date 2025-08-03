from time import sleep
import camera

FRAMESIZE_MAP = {
    "FRAME_96X96": 1, "FRAME_QQVGA": 2, "FRAME_QCIF": 3, "FRAME_HQVGA": 4,
    "FRAME_240X240": 5, "FRAME_QVGA": 6, "FRAME_CIF": 7, "FRAME_HVGA": 8,
    "FRAME_VGA": 9, "FRAME_SVGA": 10, "FRAME_XGA": 11, "FRAME_HD": 12,
    "FRAME_SXGA": 13, "FRAME_UXGA": 14, "FRAME_FHD": 15, "FRAME_P_HD": 16,
    "FRAME_P_3MP": 17, "FRAME_QXGA": 18,
}
PIXFORMAT_JPEG = 5

SPEFFECT_MAP = {
    "EFFECT_NONE": 0, "EFFECT_NEG": 1, "EFFECT_BW": 2, "EFFECT_RED": 3,
    "EFFECT_GREEN": 4, "EFFECT_BLUE": 5, "EFFECT_RETRO": 6,
}

WHITEBALANCE_MAP = {
    "WB_NONE": 0, "WB_SUNNY": 1, "WB_CLOUDY": 2, "WB_OFFICE": 3, "WB_HOME": 4,
}


class ESPCam:
    def __init__(
        self,
        frame_size,
        jpeg_quality,
        camera_flip,
        camera_mirror,
        special_effect,
        white_balance,
        contrast=0,
        brightness=0,
        saturation=0,
        agc_gain=0,
        aec_value=0,
        ae_levels=0,
    ):
        self.camera = camera
        self.frame_size = frame_size
        self.jpeg_quality = jpeg_quality
        self.camera_flip = camera_flip
        self.camera_mirror = camera_mirror
        self.contrast = contrast
        self.brightness = brightness
        self.saturation = saturation
        self.special_effect = special_effect
        self.white_balance = white_balance
        self.agc_gain = agc_gain
        self.aec_value = aec_value
        self.ae_levels = ae_levels
        self.initialized = False

    def initialize(self):
        """Initialize ESP32-CAM with settings"""
        try:
            self.camera.init()

            # Look up the integer keys for the settings
            framesize_key = FRAMESIZE_MAP.get(self.frame_size)
            speffect_key = SPEFFECT_MAP.get(self.special_effect)
            whitebalance_key = WHITEBALANCE_MAP.get(self.white_balance)

            if framesize_key is None:
                raise ValueError(f"Invalid frame size: {self.frame_size}")
            if speffect_key is None:
                raise ValueError(f"Invalid special effect: {self.special_effect}")
            if whitebalance_key is None:
                raise ValueError(f"Invalid white balance: {self.white_balance}")

            self.camera.framesize(framesize_key)
            self.camera.pixformat(PIXFORMAT_JPEG)
            self.camera.quality(self.jpeg_quality)

            # Apply additional settings from config
            if self.camera_flip:
                self.camera.flip(1)
            if self.camera_mirror:
                self.camera.mirror(1)

            self.camera.contrast(self.contrast)
            self.camera.brightness(self.brightness)
            self.camera.saturation(self.saturation)
            self.camera.speffect(speffect_key)
            self.camera.whitebalance(whitebalance_key)

            # Apply sensor settings
            self.camera.agcgain(self.agc_gain)
            self.camera.aecvalue(self.aec_value)
            self.camera.aelevels(self.ae_levels)

            sleep(5)  # Allow camera to stabilize after settings
            self.camera.capture()  # sometimes needed to apply settings

            self.initialized = True
            return True
        except Exception as e:
            print(f"Camera initialization failed: {str(e)}")
            return False

    def capture_image(self):
        """Capture an image and return the bytes"""
        if not self.initialized:
            if not self.initialize():
                return None

        try:
            buf = self.camera.capture()
            return buf
        except Exception as e:
            raise RuntimeError(f"Failed to capture image: {str(e)}")

    def get_status(self):
        """Return camera status"""
        return {
            "initialized": self.initialized,
            "frame_size": self.frame_size,
            "quality": self.jpeg_quality,
        }

    def deinitialize(self):
        """Deinitialize the camera"""
        if self.camera:
            self.camera.deinit()
            self.initialized = False
