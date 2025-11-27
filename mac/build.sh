#!/bin/bash
# Build script for Hephaestus macOS app using Swift Package Manager

set -e

cd "$(dirname "$0")"

echo "🔨 Building Hephaestus with Swift Package Manager..."
echo ""

# Build for release
swift build -c release

echo ""
echo "✅ Build complete!"
echo ""
echo "Executable location:"
echo "  .build/release/Hephaestus"
echo ""
echo "To run:"
echo "  swift run -c release"
echo ""

