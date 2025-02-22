#!/bin/bash

APP_NAME="Kasana"
VOL_NAME="Kasana"
DMG_NAME="Kasana.dmg"
TEMP_DMG_NAME="Kasana_temp.dmg"
APP_PATH="dist/Kasana.app"
DIST_FOLDER="Kasana_Dist"
BACKGROUND_IMAGE="background.png"

# Create distribution folder
mkdir "$DIST_FOLDER"
cp -R "$APP_PATH" "$DIST_FOLDER/"
ln -s /Applications "$DIST_FOLDER/Applications"

# Create temporary disk image
hdiutil create -size 100m -fs HFS+ -volname "$VOL_NAME" "$TEMP_DMG_NAME"

# Mount the temporary disk image
MOUNT_POINT=$(hdiutil attach -readwrite -noverify -noautoopen "$TEMP_DMG_NAME" | grep "/Volumes/$VOL_NAME" | awk '{print $3}')

# Copy files to disk image
cp -R "$DIST_FOLDER"/* "$MOUNT_POINT/"

# Set background image (copy to hidden .background folder)
mkdir "$MOUNT_POINT/.background"
cp "$BACKGROUND_IMAGE" "$MOUNT_POINT/.background/"

# Configure Finder window options
# (Requires AppleScript or third-party tools for advanced customization)

# Unmount the disk image
hdiutil detach "$MOUNT_POINT"

# Convert to compressed disk image
hdiutil convert "$TEMP_DMG_NAME" -format UDZO -o "$DMG_NAME"

# Remove temporary disk image and distribution folder
rm "$TEMP_DMG_NAME"
rm -rf "$DIST_FOLDER"

# Sign the disk image
codesign --force --sign "Developer ID Application: Seth Hammock (K34M384VD4)" "$DMG_NAME"

# Notarize the disk image
xcrun notarytool submit "$DMG_NAME" --apple-id your-apple-id@example.com --team-id K34M384VD4 --password app-specific-password --wait

# Staple the notarization ticket
xcrun stapler staple "$DMG_NAME"

# Verify stapling
xcrun stapler validate "$DMG_NAME"