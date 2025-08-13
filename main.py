from lib.microdot_asyncio import Microdot, Response
import machine
import config
from webcam import ESPCam
import gc
import ubinascii

# Initialize flash LED and create camera instance (but don't initialize yet)
flash = machine.Pin(4, machine.Pin.OUT)
camera = ESPCam(
    frame_size=config.CAMERA_FRAME_SIZE,
    jpeg_quality=config.CAMERA_JPEG_QUALITY,
    camera_flip=config.CAMERA_FLIP,
    camera_mirror=config.CAMERA_MIRROR,
    contrast=config.CAMERA_CONTRAST,
    brightness=config.CAMERA_BRIGHTNESS,
    saturation=config.CAMERA_SATURATION,
    special_effect=config.CAMERA_SPECIAL_EFFECT,
    white_balance=config.CAMERA_WHITE_BALANCE,
    agc_gain=config.CAMERA_AGC_GAIN,
    aec_value=config.CAMERA_AEC_VALUE,
    ae_levels=config.CAMERA_AE_LEVELS,
)
app = Microdot()


@app.route("/")
async def index(request):
    return {"status": "ok"}, 200, {"Content-Type": "application/json"}


def _capture_image(use_flash=False):
    """Internal function to capture an image."""
    buf = None
    try:
        if not camera.initialize():
            raise Exception("Failed to initialize camera")

        if use_flash:
            flash.on()

        # Capture the image
        try:
            buf = camera.capture_image()
            if buf is None:
                raise Exception("Failed to capture image: Buffer is None")
            return buf
        except Exception as e:
            raise Exception(f"Failed to capture image: {str(e)}")
    finally:
        if use_flash:
            flash.off()

        # Deinitialize camera after capture
        # This releases the camera hardware resources and PSRAM frame buffer
        camera.deinitialize()

        # Explicitly delete the buffer reference and run garbage collection.
        if buf is not None:
            del buf
        gc.collect()


@app.route("/capture")
async def capture(request):
    use_flash = request.args.get("flash", "false").lower() == "true"

    # Capture the image
    try:
        img_binary = _capture_image(use_flash=use_flash)
        # Return the image as a JPEG response
        return Response(body=img_binary, headers={"Content-Type": "image/jpeg"})

    except Exception as e:
        return {"error": str(e)}, 503, {"Content-Type": "application/json"}


@app.route("/capture_base64")
async def capture_base64(request):
    use_flash = request.args.get("flash", "false").lower() == "true"

    # Capture the image
    try:
        img_binary = _capture_image(use_flash=use_flash)
        # Encode the image buffer to a base64 string
        encoded_image = ubinascii.b2a_base64(img_binary).decode("utf-8").strip()
        # Return the base64 encoded image as a plain text response
        return Response(body=encoded_image, headers={"Content-Type": "text/plain"})
    except Exception as e:
        return str(e), 503, {"Content-Type": "text/plain"}


@app.route("/status")
async def status(request):
    return (
        {
            "flash_available": True,
            "camera": camera.get_status(),
            "effects": {
                "flip": config.CAMERA_FLIP,
                "mirror": config.CAMERA_MIRROR,
                "contrast": config.CAMERA_CONTRAST,
                "brightness": config.CAMERA_BRIGHTNESS,
                "saturation": config.CAMERA_SATURATION,
                "agc_gain": config.CAMERA_AGC_GAIN,
                "aec_value": config.CAMERA_AEC_VALUE,
                "ae_levels": config.CAMERA_AE_LEVELS,
            },
        },
        200,
        {"Content-Type": "application/json"},
    )


def main():
    if not IP_ADDRESS:
        print("Failed to connect to WiFi. Cannot start server.")
        return

    print(f"Server started at http://{IP_ADDRESS}")
    app.run(host=IP_ADDRESS, port=config.PORT, debug=True)


if __name__ == "__main__":
    main()
