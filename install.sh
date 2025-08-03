#!/bin/bash

# --- Configuration ---
# Set your ESP32's serial port. Use 'auto' if mpremote can detect it.
# Examples: "auto", "COM3", "/dev/ttyUSB0", "/dev/ttyACM0"
ESP32_PORT="auto"

# Set the path to your local MicroPython project directory
LOCAL_PROJECT_DIR="." # Adjust this to your actual folder name/path

# --- Script Start ---

echo "----------------------------------------------------"
echo "  ESP32 Cam MicroPython REST API Installer"
echo "----------------------------------------------------"
echo ""
echo "WARNING: This script will DELETE ALL FILES on your ESP32's MicroPython filesystem."
echo "         (It will NOT delete the MicroPython firmware itself)."
echo ""
echo "Ensure you have backed up any important files before proceeding!"
echo ""
read -p "Type 'yes' to continue with file deletion: " CONFIRMATION

if [ "$CONFIRMATION" != "yes" ]; then
    echo "Deletion cancelled. Exiting."
    exit 0
fi

echo ""
echo "Connecting to ESP32 on port: $ESP32_PORT"
echo "Deleting all files on ESP32..."

# Delete everything from the root of the ESP32's filesystem
mpremote connect "$ESP32_PORT" rm -r :/

# Check if the deletion command was successful
if [ $? -eq 0 ]; then
    echo "Successfully deleted all files on ESP32."
else
    echo "Error during file deletion. Please check the output above."
    echo "Attempting to continue with upload, but issues may persist."
fi

echo ""
echo "Waiting a moment for the device to settle..."
sleep 2

echo "Starting file upload from '$LOCAL_PROJECT_DIR' to ESP32..."

mpremote connect "$ESP32_PORT" cp "$LOCAL_PROJECT_DIR/.env" :".env"
mpremote connect "$ESP32_PORT" cp "$LOCAL_PROJECT_DIR/config.py" :"config.py"
mpremote connect "$ESP32_PORT" mkdir lib
mpremote connect "$ESP32_PORT" cp "$LOCAL_PROJECT_DIR/lib/microdot.py" :"lib/microdot.py"
mpremote connect "$ESP32_PORT" cp "$LOCAL_PROJECT_DIR/lib/microdot_asyncio.py" :"lib/microdot_asyncio.py"
mpremote connect "$ESP32_PORT" cp "$LOCAL_PROJECT_DIR/webcam.py" :"webcam.py"
mpremote connect "$ESP32_PORT" cp "$LOCAL_PROJECT_DIR/main.py" :"main.py"
mpremote connect "$ESP32_PORT" cp "$LOCAL_PROJECT_DIR/boot.py" :"boot.py"

echo ""
echo "File upload complete."
echo "Resetting ESP32 and entering REPL to monitor boot-up and interact."
echo "Press Ctrl+D to soft-reset the ESP32 once in REPL."
echo "Press Ctrl+X to exit mpremote REPL."

# Enter REPL after upload to see the device boot and for further interaction
mpremote connect "$ESP32_PORT" repl

echo "Script finished."
echo "----------------------------------------------------"