// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "Hephaestus",
    platforms: [
        .macOS(.v12)
    ],
    products: [
        .executable(
            name: "Hephaestus",
            targets: ["Hephaestus"]
        )
    ],
    targets: [
        .executableTarget(
            name: "Hephaestus"
        )
    ]
)

