from lib.microdot import Microdot, Response
import machine
import uasyncio as asyncio
import config
from webcam import ESPCam
import gc

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
)
app = Microdot()


@app.route("/")
async def index(request):
    return {"status": "ok"}, 200, {"Content-Type": "application/json"}


@app.route("/capture")
async def capture(request):
    buf = None
    try:
        use_flash = request.args.get("flash", "false").lower() == "true"

        if not camera.initialize():
            return {"error": "Failed to initialize camera"}, 503

        if use_flash:
            flash.on()

        # Wait for sensor to start and focus
        await asyncio.sleep(2)

        # Capture the image
        try:
            buf = camera.capture_image()
            # Return the image as a JPEG response
            return Response(body=buf, headers={"Content-Type": "image/jpeg"})
        except Exception as e:
            return {"error": str(e)}, 503, {"Content-Type": "application/json"}

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
