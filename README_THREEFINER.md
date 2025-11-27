# Threefiner Integration Guide

Hephaestus now includes seamless integration with [threefiner](https://github.com/3DTopia/threefiner) for automatic mesh refinement. Transform your rough-forged creations into flawless masterworks with a single flag.

## Quick Start

### Automatic Refinement

Simply add `--refine` to automatically refine your generated meshes:

```bash
python -u sample_stage1.py \
  --text "a majestic dragon statue" \
  --samples 1 \
  --sampler ddim \
  --steps 200 \
  --refine \
  --refine_mode if2 \
  --refine_iters 1000
```

This will:
1. Generate the initial 3D model (Stage 1)
2. **Automatically** refine it with threefiner (Stage 2)
3. Output both the original and refined models

### Output Structure

```
results/
  default/
    stage1/
      your_model_0_0.ply          # Original mesh
      your_model_0_0.mp4          # Rotation video
    stage2/
      your_model_0_0_refined.glb  # ✨ Flawless refined mesh
```

## Refinement Modes

Choose the refinement mode that best suits your needs:

- **`if2`** (Recommended) - Deepfloyd-IF-II, best quality, handles both geometry and texture
- **`sd`** - Stable Diffusion refinement, good for textures
- **`if`** - Deepfloyd-IF refinement
- **`if2_fixgeo`** - IF2 with geometry fixing
- **`sd_fixgeo`** - SD with geometry fixing
- **`if_fixgeo`** - IF with geometry fixing

### High Quality Settings

For the best possible results, use:

```bash
--refine --refine_mode if2 --refine_iters 1000
```

This uses Deepfloyd-IF-II with 1000 iterations for maximum quality. Generation will take longer but the results will be flawless.

## Installation

### Prerequisites

Threefiner requires CUDA (Linux/Windows with NVIDIA GPU). It cannot run on Mac MPS.

1. **Install threefiner:**
   ```bash
   pip install threefiner
   ```

2. **Install CUDA dependencies:**
   ```bash
   # tiny-cuda-nn
   pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
   
   # nvdiffrast
   pip install git+https://github.com/NVlabs/nvdiffrast
   
   # [optional] cubvh
   pip install git+https://github.com/ashawkey/cubvh
   ```

3. **HuggingFace Setup:**
   For Deepfloyd-IF models, log in to HuggingFace and accept the license:
   ```bash
   huggingface-cli login
   ```

### Verify Installation

Check if threefiner is available:

```bash
threefiner --help
```

## Usage Examples

### Quick Refinement (400 iterations)

```bash
python -u sample_stage1.py \
  --text "a cute robot" \
  --samples 1 \
  --refine \
  --refine_iters 400
```

### Flawless Quality (1000 iterations)

```bash
python -u sample_stage1.py \
  --text "a detailed pocket watch" \
  --samples 1 \
  --sampler ddim \
  --steps 200 \
  --refine \
  --refine_mode if2 \
  --refine_iters 1000
```

### Geometry + Texture Fix

```bash
python -u sample_stage1.py \
  --text "a vintage car" \
  --samples 1 \
  --refine \
  --refine_mode if2_fixgeo \
  --refine_iters 1000
```

## Mac Users

**Important:** Threefiner requires CUDA and cannot run on Mac MPS. 

However, you can:
1. Generate models on Mac (Stage 1 works perfectly)
2. Transfer the `.ply` files to a CUDA machine
3. Run refinement manually:
   ```bash
   threefiner if2 --mesh your_model.ply --prompt "your prompt" --outdir . --save refined.glb
   ```

Or use the refinement utility directly:

```python
from utility.refinement import refine_with_threefiner

refined_path = refine_with_threefiner(
    mesh_path="your_model.ply",
    prompt="a cute robot",
    refinement_mode="if2",
    iters=1000
)
```

## Troubleshooting

### "threefiner CLI not found"

Install threefiner:
```bash
pip install threefiner
```

### "CUDA not available"

Threefiner requires CUDA (NVIDIA GPU on Linux/Windows). Mac MPS is not supported.

### "Failed to convert PLY to GLB"

The PLY to GLB conversion should work automatically. If it fails, you can manually convert:
```python
import trimesh
mesh = trimesh.load("model.ply")
mesh.export("model.glb", file_type='glb')
```

### Refinement Takes Too Long

- Reduce `--refine_iters` (e.g., 400 instead of 1000)
- Use `sd` mode instead of `if2` for faster refinement
- Skip refinement entirely if quality is acceptable

## Performance

- **Stage 1 (Generation):** ~15-30 seconds (on Mac MPS)
- **Stage 2 (Refinement):** 
  - 400 iterations: ~1-2 minutes
  - 1000 iterations: ~3-5 minutes

**Total with refinement:** ~3-6 minutes for a flawless 3D model

## Integration Details

Hephaestus automatically:
- Converts PLY meshes to GLB format (required by threefiner)
- Checks if threefiner and CUDA are available
- Runs refinement in a separate directory (`stage2/`)
- Preserves original meshes in `stage1/`
- Provides clear feedback on the refinement process

The refinement is completely optional—your workflow works perfectly without it, but with it, you get production-ready, flawless models every time.

---

*For more information about threefiner, visit: https://github.com/3DTopia/threefiner*

