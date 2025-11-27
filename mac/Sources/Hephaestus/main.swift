//
//  HephaestusApp.swift
//  Hephaestus - 3D Model Generator
//
//  A beautiful SwiftUI interface for forging 3D models with AI
//

import SwiftUI

@main
struct HephaestusApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 1000, minHeight: 700)
        }
        .windowStyle(.hiddenTitleBar)
        .windowToolbarStyle(.unified)
        .commands {
            // App menu customization
        }
    }
    
    init() {
        // Set app icon if possible
        if let iconPath = Bundle.main.path(forResource: "Hephaestus", ofType: "png") {
            // Icon will be set via Assets.xcassets in Xcode project
        }
    }
}

struct ContentView: View {
    @StateObject private var generator = ModelGenerator()
    
    var body: some View {
        HSplitView {
            // Left Panel: Controls
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    HeaderView()
                    
                    // Prompt Section
                    PromptSection(generator: generator)
                    
                    // Generation Settings
                    GenerationSettingsSection(generator: generator)
                    
                    // Sampling Settings
                    SamplingSettingsSection(generator: generator)
                    
                    // Mesh Settings
                    MeshSettingsSection(generator: generator)
                    
                    // Refinement Settings
                    RefinementSettingsSection(generator: generator)
                    
                    // Advanced Settings
                    AdvancedSettingsSection(generator: generator)
                    
                    // Generate Button
                    GenerateButton(generator: generator)
                }
                .padding(24)
            }
            .frame(minWidth: 480, idealWidth: 500)
            .background(Color(NSColor.controlBackgroundColor))
            
            // Right Panel: Output & Progress
            OutputPanel(generator: generator)
                .frame(minWidth: 500)
        }
    }
}

// MARK: - Header

struct HeaderView: View {
    @State private var logoImage: NSImage? = nil
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(spacing: 16) {
                // Hephaestus Logo
                Group {
                    if let image = logoImage {
                        Image(nsImage: image)
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                    } else {
                        Image(systemName: "hammer.fill")
                            .font(.system(size: 32))
                            .foregroundColor(.orange)
                    }
                }
                .frame(width: 64, height: 64)
                .cornerRadius(12)
                .shadow(color: .black.opacity(0.1), radius: 4, x: 0, y: 2)
                .onAppear {
                    loadLogo()
                }
                
                VStack(alignment: .leading, spacing: 4) {
                    Text("Hephaestus")
                        .font(.system(size: 32, weight: .bold))
                        .foregroundColor(.primary)
                    
                    Text("Forge 3D Models from Text")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding(.bottom, 8)
    }
    
    private func loadLogo() {
        let logoPath = "/Users/caraveo/Hephaestus/Hephaestus.png"
        if let image = NSImage(contentsOfFile: logoPath) {
            logoImage = image
        }
    }
}

// MARK: - Prompt Section

struct PromptSection: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        SettingsCard(title: "Text Prompt", icon: "text.bubble.fill", color: .blue) {
            VStack(alignment: .leading, spacing: 12) {
                TextField("e.g., a majestic dragon statue", text: $generator.prompt, axis: .vertical)
                    .textFieldStyle(.roundedBorder)
                    .lineLimit(3...6)
                
                InfoRow(
                    title: "Description",
                    description: "Describe the 3D object you want to create. Be creative and specific!"
                )
            }
        }
    }
}

// MARK: - Generation Settings

struct GenerationSettingsSection: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        SettingsCard(title: "Generation Settings", icon: "gearshape.fill", color: .purple) {
            VStack(alignment: .leading, spacing: 16) {
                // Number of Samples
                SliderControl(
                    title: "Number of Variations",
                    value: $generator.samples,
                    range: 1...4,
                    step: 1,
                    description: "Generate multiple variations to choose from. More samples = more options but longer generation time."
                )
                
                Divider()
                
                // Seed
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Text("Random Seed")
                            .font(.headline)
                        Spacer()
                        TextField("Auto", value: $generator.seed, format: .number)
                            .textFieldStyle(.roundedBorder)
                            .frame(width: 80)
                    }
                    
                    InfoRow(
                        title: "Description",
                        description: "Control randomness for reproducible results. Leave empty for random generation each time."
                    )
                }
            }
        }
    }
}

// MARK: - Sampling Settings

struct SamplingSettingsSection: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        SettingsCard(title: "Sampling Settings", icon: "slider.horizontal.3", color: .green) {
            VStack(alignment: .leading, spacing: 16) {
                // Sampler Type
                PickerControl(
                    title: "Sampler Algorithm",
                    selection: $generator.sampler,
                    options: [
                        ("ddim", "DDIM - Fast and efficient, recommended for most cases"),
                        ("plms", "PLMS - Pseudo Linear Multistep, good balance"),
                        ("dpm_solver", "DPM Solver - Advanced solver for high quality")
                    ],
                    description: "Different algorithms for the diffusion process. DDIM is fastest, DPM Solver is highest quality."
                )
                
                Divider()
                
                // Steps
                SliderControl(
                    title: "Sampling Steps",
                    value: $generator.steps,
                    range: 10...1000,
                    step: 10,
                    description: "More steps = higher quality but slower generation. 50-200 is usually sufficient."
                )
                
                Divider()
                
                // CFG Scale
                SliderControl(
                    title: "Guidance Scale",
                    value: $generator.cfgScale,
                    range: 1.0...15.0,
                    step: 0.5,
                    description: "How closely to follow your prompt. Higher = more adherence but may reduce creativity. 7.5 is recommended."
                )
            }
        }
    }
}

// MARK: - Mesh Settings

struct MeshSettingsSection: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        SettingsCard(title: "Mesh Settings", icon: "cube.fill", color: .cyan) {
            VStack(alignment: .leading, spacing: 16) {
                // Marching Cubes Resolution
                SliderControl(
                    title: "Mesh Resolution",
                    value: $generator.mcubesRes,
                    range: 64...256,
                    step: 32,
                    description: "Higher resolution = more detailed mesh but uses more memory. 128 is a good balance."
                )
                
                Divider()
                
                // Render Resolution
                SliderControl(
                    title: "Video Resolution",
                    value: $generator.renderRes,
                    range: 64...256,
                    step: 32,
                    description: "Resolution for rotation videos. Higher = better quality but larger files."
                )
                
                Divider()
                
                // Video Toggle
                ToggleControl(
                    title: "Generate Rotation Video",
                    isOn: $generator.generateVideo,
                    description: "Create an MP4 video showing your model rotating 360°"
                )
            }
        }
    }
}

// MARK: - Refinement Settings

struct RefinementSettingsSection: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        SettingsCard(title: "Flawless Refinement", icon: "sparkles", color: .orange) {
            VStack(alignment: .leading, spacing: 16) {
                // Refinement Toggle
                ToggleControl(
                    title: "Enable Refinement",
                    isOn: $generator.enableRefinement,
                    description: "Automatically refine your mesh for production-ready quality. Works natively on Mac!"
                )
                
                if generator.enableRefinement {
                    Divider()
                    
                    // Refinement Mode (only if CUDA available)
                    PickerControl(
                        title: "Refinement Mode",
                        selection: $generator.refineMode,
                        options: [
                            ("if2", "Deepfloyd-IF-II - Best quality, handles geometry and texture"),
                            ("sd", "Stable Diffusion - Good for texture refinement"),
                            ("if", "Deepfloyd-IF - Alternative refinement method"),
                            ("if2_fixgeo", "IF2 + Geometry Fix - Fixes geometry while refining"),
                            ("sd_fixgeo", "SD + Geometry Fix - SD with geometry improvements"),
                            ("if_fixgeo", "IF + Geometry Fix - IF with geometry improvements")
                        ],
                        description: "Mac uses native MPS refinement automatically. CUDA users can choose threefiner modes."
                    )
                    
                    Divider()
                    
                    // Refinement Iterations
                    SliderControl(
                        title: "Refinement Iterations",
                        value: $generator.refineIters,
                        range: 100...2000,
                        step: 100,
                        description: "More iterations = better quality but longer refinement time. 1000 is recommended for high quality."
                    )
                }
            }
        }
    }
}

// MARK: - Advanced Settings

struct AdvancedSettingsSection: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        SettingsCard(title: "Advanced", icon: "wrench.and.screwdriver.fill", color: .gray) {
            VStack(alignment: .leading, spacing: 12) {
                ToggleControl(
                    title: "Skip Mesh Generation",
                    isOn: $generator.skipMesh,
                    description: "Only generate the latent representation, skip mesh extraction (for testing)"
                )
            }
        }
    }
}

// MARK: - Generate Button

struct GenerateButton: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        Button(action: {
            generator.generate()
        }) {
            HStack {
                if generator.isGenerating {
                    ProgressView()
                        .scaleEffect(0.8)
                } else {
                    Image(systemName: "hammer.fill")
                }
                
                Text(generator.isGenerating ? "Forging..." : "Forge 3D Model")
                    .fontWeight(.semibold)
            }
            .frame(maxWidth: .infinity)
            .frame(height: 44)
        }
        .buttonStyle(.borderedProminent)
        .controlSize(.large)
        .disabled(generator.isGenerating || generator.prompt.isEmpty)
        .padding(.top, 8)
    }
}

// MARK: - Output Panel

struct OutputPanel: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                Text("Output")
                    .font(.headline)
                Spacer()
                if generator.isGenerating {
                    ProgressView()
                }
            }
            .padding()
            .background(Color(NSColor.separatorColor).opacity(0.2))
            
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    // Progress
                    if generator.isGenerating {
                        ProgressSection(generator: generator)
                    }
                    
                    // Log Output
                    LogView(generator: generator)
                    
                    // Results
                    if !generator.outputFiles.isEmpty {
                        ResultsView(generator: generator)
                    }
                }
                .padding()
            }
        }
        .background(Color(NSColor.textBackgroundColor))
    }
}

// MARK: - Progress Section

struct ProgressSection: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Progress")
                .font(.headline)
            
            if let currentStep = generator.currentStep {
                ProgressView(value: generator.progress) {
                    Text(currentStep)
                        .font(.subheadline)
                }
                
                if let details = generator.stepDetails {
                    Text(details)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(8)
    }
}

// MARK: - Log View

struct LogView: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Generation Log")
                .font(.headline)
            
            ScrollView {
                Text(generator.logOutput)
                    .font(.system(.caption, design: .monospaced))
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(8)
                    .background(Color.black.opacity(0.05))
                    .cornerRadius(4)
            }
            .frame(height: 200)
        }
    }
}

// MARK: - Results View

struct ResultsView: View {
    @ObservedObject var generator: ModelGenerator
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Generated Files")
                .font(.headline)
            
            ForEach(generator.outputFiles, id: \.self) { file in
                HStack {
                    Image(systemName: fileIcon(for: file))
                        .foregroundColor(.blue)
                    
                    Text(file)
                        .font(.subheadline)
                    
                    Spacer()
                    
                    Button("Reveal") {
                        revealInFinder(file: file)
                    }
                    .buttonStyle(.borderless)
                }
                .padding(8)
                .background(Color(NSColor.controlBackgroundColor))
                .cornerRadius(6)
            }
        }
    }
    
    private func fileIcon(for file: String) -> String {
        if file.hasSuffix(".ply") { return "cube.fill" }
        if file.hasSuffix(".mp4") { return "video.fill" }
        if file.hasSuffix(".glb") { return "cube.box.fill" }
        return "doc.fill"
    }
    
    private func revealInFinder(file: String) {
        let url = URL(fileURLWithPath: file)
        NSWorkspace.shared.activateFileViewerSelecting([url])
    }
}

// MARK: - Reusable Components

struct SettingsCard<Content: View>: View {
    let title: String
    let icon: String
    let color: Color
    let content: () -> Content
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(color)
                    .font(.headline)
                Text(title)
                    .font(.headline)
            }
            
            Divider()
            
            content()
        }
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(12)
    }
}

struct InfoRow: View {
    let title: String
    let description: String
    
    var body: some View {
        HStack(alignment: .top, spacing: 8) {
            Image(systemName: "info.circle.fill")
                .foregroundColor(.blue)
                .font(.caption)
            
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.caption)
                    .fontWeight(.semibold)
                Text(description)
                    .font(.caption2)
                    .foregroundColor(.secondary)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }
}

struct SliderControl: View {
    let title: String
    @Binding var value: Double
    let range: ClosedRange<Double>
    let step: Double
    let description: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(title)
                    .font(.headline)
                Spacer()
                Text("\(Int(value))")
                    .font(.headline)
                    .foregroundColor(.secondary)
                    .monospacedDigit()
            }
            
            Slider(value: $value, in: range, step: step)
            
            InfoRow(
                title: "How it works",
                description: description
            )
        }
    }
}

struct PickerControl: View {
    let title: String
    @Binding var selection: String
    let options: [(String, String)]
    let description: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.headline)
            
            Picker("", selection: $selection) {
                ForEach(options, id: \.0) { option in
                    Text(option.0.uppercased()).tag(option.0)
                }
            }
            .pickerStyle(.menu)
            
            if let selectedOption = options.first(where: { $0.0 == selection }) {
                InfoRow(
                    title: selectedOption.0.uppercased(),
                    description: selectedOption.1
                )
            }
            
            InfoRow(
                title: "How it works",
                description: description
            )
        }
    }
}

struct ToggleControl: View {
    let title: String
    @Binding var isOn: Bool
    let description: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Toggle(title, isOn: $isOn)
                .font(.headline)
            
            InfoRow(
                title: "Description",
                description: description
            )
        }
    }
}

// MARK: - Model Generator

class ModelGenerator: ObservableObject {
    @Published var prompt: String = "a cute robot"
    @Published var samples: Double = 1
    @Published var seed: Int? = nil
    @Published var sampler: String = "ddim"
    @Published var steps: Double = 200
    @Published var cfgScale: Double = 7.5
    @Published var mcubesRes: Double = 128
    @Published var renderRes: Double = 128
    @Published var generateVideo: Bool = true
    @Published var enableRefinement: Bool = false
    @Published var refineMode: String = "if2"
    @Published var refineIters: Double = 1000
    @Published var skipMesh: Bool = false
    
    @Published var isGenerating: Bool = false
    @Published var progress: Double = 0.0
    @Published var currentStep: String? = nil
    @Published var stepDetails: String? = nil
    @Published var logOutput: String = ""
    @Published var outputFiles: [String] = []
    
    func generate() {
        isGenerating = true
        logOutput = ""
        outputFiles = []
        progress = 0.0
        
        // Build command
        var command = "python -u sample_stage1.py"
        command += " --text \"\(prompt)\""
        command += " --samples \(Int(samples))"
        command += " --sampler \(sampler)"
        command += " --steps \(Int(steps))"
        command += " --cfg_scale \(cfgScale)"
        command += " --mcubes_res \(Int(mcubesRes))"
        command += " --render_res \(Int(renderRes))"
        
        if let seed = seed {
            command += " --seed \(seed)"
        }
        
        if !generateVideo {
            command += " --no_video"
        }
        
        if skipMesh {
            command += " --no_mcubes"
        }
        
        if enableRefinement {
            command += " --refine"
            command += " --refine_mode \(refineMode)"
            command += " --refine_iters \(Int(refineIters))"
        }
        
        logOutput += "Command: \(command)\n\n"
        currentStep = "Initializing..."
        
        // Execute command asynchronously
        Task {
            await executeCommand(command)
        }
    }
    
    @MainActor
    private func executeCommand(_ command: String) async {
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/bin/zsh")
        process.arguments = ["-c", "cd /Users/caraveo/Hephaestus && source activate_hephaestus.sh && \(command)"]
        
        let pipe = Pipe()
        process.standardOutput = pipe
        process.standardError = pipe
        
        let outputHandle = pipe.fileHandleForReading
        
        outputHandle.readabilityHandler = { handle in
            let data = handle.availableData
            if !data.isEmpty {
                if let string = String(data: data, encoding: .utf8) {
                    Task { @MainActor in
                        self.logOutput += string
                        
                        // Update progress based on log
                        if string.contains("DDIM Sampler:") {
                            self.currentStep = "Generating 3D model..."
                            // Extract progress from log if possible
                        } else if string.contains("marching cube") {
                            self.currentStep = "Extracting mesh..."
                            self.progress = 0.6
                        } else if string.contains("refinement") {
                            self.currentStep = "Refining mesh..."
                            self.progress = 0.8
                        } else if string.contains("Generated mesh:") || string.contains("Refined mesh:") {
                            // Extract file path
                            if let filePath = extractFilePath(from: string) {
                                self.outputFiles.append(filePath)
                            }
                        }
                    }
                }
            }
        }
        
        do {
            try process.run()
            process.waitUntilExit()
            
            await MainActor.run {
                progress = 1.0
                currentStep = "Complete!"
                isGenerating = false
                
                // Find output files
                scanForOutputFiles()
            }
        } catch {
            await MainActor.run {
                logOutput += "\nError: \(error.localizedDescription)\n"
                isGenerating = false
            }
        }
    }
    
    private func extractFilePath(from line: String) -> String? {
        // Extract file path from log line
        if let range = line.range(of: "results/") {
            let path = String(line[range.lowerBound...])
            if let endRange = path.range(of: "\n") {
                return String(path[..<endRange.lowerBound]).trimmingCharacters(in: .whitespacesAndNewlines)
            }
            return path.trimmingCharacters(in: .whitespacesAndNewlines)
        }
        return nil
    }
    
    private func scanForOutputFiles() {
        let resultsDir = "/Users/caraveo/Hephaestus/results/default"
        let fileManager = FileManager.default
        
        if let stage1Files = try? fileManager.contentsOfDirectory(atPath: "\(resultsDir)/stage1") {
            for file in stage1Files where file.hasSuffix(".ply") || file.hasSuffix(".mp4") {
                outputFiles.append("\(resultsDir)/stage1/\(file)")
            }
        }
        
        if let stage2Files = try? fileManager.contentsOfDirectory(atPath: "\(resultsDir)/stage2") {
            for file in stage2Files where file.hasSuffix(".ply") || file.hasSuffix(".glb") {
                outputFiles.append("\(resultsDir)/stage2/\(file)")
            }
        }
    }
}

