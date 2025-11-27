# Building Hephaestus macOS App

## Prerequisites

- macOS 12.3 or later
- Xcode 14.0 or later
- Swift 5.0+

## Building with Xcode

1. Open the project:
   ```bash
   open mac/Hephaestus.xcodeproj
   ```

2. Select the scheme: **Hephaestus**

3. Select the destination: **My Mac**

4. Build for Release:
   - Product → Scheme → Edit Scheme
   - Set Build Configuration to **Release**
   - Product → Build (⌘B)

5. Archive for Distribution:
   - Product → Archive
   - Distribute App
   - Choose distribution method (App Store, Ad Hoc, or Direct)

## Building from Command Line

```bash
cd mac
xcodebuild -project Hephaestus.xcodeproj \
           -scheme Hephaestus \
           -configuration Release \
           -derivedDataPath ./build \
           clean build
```

The built app will be at: `mac/build/Build/Products/Release/Hephaestus.app`

## Building a Release Archive

```bash
cd mac
xcodebuild -project Hephaestus.xcodeproj \
           -scheme Hephaestus \
           -configuration Release \
           archive \
           -archivePath ./build/Hephaestus.xcarchive
```

## Creating a DMG for Distribution

After building, create a DMG:

```bash
# Create DMG
hdiutil create -volname "Hephaestus" \
               -srcfolder "mac/build/Build/Products/Release/Hephaestus.app" \
               -ov -format UDZO \
               Hephaestus.dmg
```

## Notes

- The app requires the Hephaestus Python environment to be installed
- Make sure `activate_hephaestus.sh` is accessible
- The app will execute Python scripts from the Hephaestus directory

