import camera


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
        self.initialized = False

    def initialize(self):
        """Initialize ESP32-CAM with settings"""
        try:
            import esp

            if not esp.flash_size() > 0:  # Check for PSRAM
                print("Error: PSRAM not found")
                return False
            self.camera.deinit()  # Ensure camera is deinitialized before reinitializing
            # Initialize camera with PSRAM frame buffer
            self.camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)

            # Apply image settings
            self.camera.framesize(getattr(camera, self.frame_size))
            self.camera.quality(self.jpeg_quality)

            # Apply additional settings from config
            if self.camera_flip:
                self.camera.flip(1)
            if self.camera_mirror:
                self.camera.mirror(1)

            self.camera.contrast(self.contrast)
            self.camera.brightness(self.brightness)
            self.camera.saturation(self.saturation)

            # Apply special effects if specified
            if self.special_effect:
                effect = getattr(camera, self.special_effect)
                self.camera.speffect(effect)

            # Apply white balance if specified
            if self.white_balance:
                wb = getattr(camera, self.white_balance)
                self.camera.whitebalance(wb)

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
