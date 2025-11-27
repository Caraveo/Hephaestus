# Hephaestus - Mac MPS Setup Guide

This guide will help you set up Hephaestus (3DTopia) to run on macOS using Metal Performance Shaders (MPS) with float16 precision.

## Prerequisites

- macOS 12.3 or later (for MPS support)
- Apple Silicon (M1/M2/M3) or Intel Mac with Apple Silicon support
- Python 3.10+
- Anaconda or Miniconda

## Installation

### 1. Create the Conda Environment

```bash
conda env create -f environment_mac.yml
conda activate hephaestus
```

### 2. Verify MPS Support

Run the following to check if MPS is available:

```python
import torch
print(f"MPS available: {torch.backends.mps.is_available()}")
print(f"MPS built: {torch.backends.mps.is_built()}")
```

### 3. Download Model Checkpoints

The model checkpoints will be automatically downloaded on first run, or you can download them manually from [HuggingFace](https://huggingface.co/hongfz16/3DTopia).

## Usage

### Stage 1: Generate Initial 3D Models

```bash
python -u sample_stage1.py --text "a robot" --samples 1 --sampler ddim --steps 200 --cfg_scale 7.5 --seed 0
```

### Stage 2: Refinement (Optional)

Please refer to [threefiner](https://github.com/3DTopia/threefiner) for second stage mesh refinement.

### Gradio Demo

```bash
python gradio_demo.py
```

The demo will automatically:
- Use MPS device if available
- Convert models to float16 for MPS
- Handle device-agnostic memory management

## Important Notes

### Memory Management

- MPS uses system memory, so ensure you have sufficient RAM
- For large models, you may need to reduce batch sizes or resolution
- Use `--mcubes_res 64` or `--render_res 64` to reduce memory usage if needed

### Performance

- First run may be slower due to model compilation
- MPS performance is optimized for Apple Silicon
- Float16 precision may have slight quality differences compared to float32

### Troubleshooting

1. **OpenMP Error**: If you see "Error #15: Initializing libomp.dylib", this is a common Mac issue. The scripts automatically set `KMP_DUPLICATE_LIB_OK=TRUE` to work around this. If you still see the error, run:
   ```bash
   export KMP_DUPLICATE_LIB_OK=TRUE
   ```
   Or use the activation script: `source activate_hephaestus.sh`

2. **MPS not available**: Update PyTorch to latest version (>=2.0.0)

3. **Out of memory**: Reduce `--mcubes_res` and `--render_res` parameters

4. **Import errors**: Ensure all dependencies are installed from the environment file

## Configuration

The system automatically detects and uses:
- MPS (Metal Performance Shaders) on Mac
- CUDA on systems with NVIDIA GPUs
- CPU as fallback

Device selection happens automatically via `utility/device_utils.py`.

## Known Limitations

- Second stage refinement (threefiner) may require additional setup
- Some operations may fall back to CPU if not supported by MPS
- Maximum tensor size limits may be different on MPS

