#!/bin/bash

# Build script for Kasana app

# Exit immediately if a command exits with a non-zero status
set -e

# Clean previous builds and build the app using PyInstaller
echo "Building the app with PyInstaller..."
pyinstaller --clean Kasana.spec

# Change to the dist directory
cd dist

# Codesign the app
echo "Codesigning the app..."
codesign --deep --force --verbose --options runtime \
--entitlements ../entitlements.plist \
--sign "Developer ID Application: Seth Hammock (K34M384VD4)" Kasana.app

# Set permissions on the app
echo "Setting permissions on the app..."
sudo chmod -R 755 Kasana.app

# Re-codesign the executable files inside the app
echo "Codesigning the executable files inside the app..."
find "Kasana.app/Contents/MacOS" -type f -exec codesign --force --sign "Developer ID Application: Seth Hammock (K34M384VD4)" --options runtime --entitlements "../entitlements.plist" {} \;

# Codesign the app again
echo "Codesigning the app again..."
codesign --force --deep --options runtime --sign "Developer ID Application: Seth Hammock (K34M384VD4)" --entitlements "../entitlements.plist" "Kasana.app"

echo "Build and codesigning completed successfully."