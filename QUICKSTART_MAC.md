# Quick Start Guide for Mac (Hephaestus)

## Installation (5 minutes)

1. **Clone and setup environment:**
```bash
cd Hephaestus
conda env create -f environment_mac.yml
conda activate hephaestus
```

2. **Verify MPS support:**
```bash
python test_mps.py
```

You should see:
- ✓ MPS available: True
- ✓ All tests passed!

## First Run

Generate your first 3D model:
```bash
python -u sample_stage1.py --text "a cute robot" --samples 1 --sampler ddim --steps 200 --cfg_scale 7.5 --seed 0
```

Results will be in `results/default/stage1/`

## Optional: Gradio Web Interface

```bash
python gradio_demo.py
```

Note: The gradio demo requires `threefiner` for stage 2 refinement. Install separately if needed.

## Troubleshooting

- **MPS not available?** Update PyTorch: `pip install torch --upgrade`
- **Out of memory?** Use lower resolution: `--mcubes_res 64 --render_res 64`
- **Import errors?** Make sure you're in the conda environment: `conda activate hephaestus`

## Performance Tips

- First run is slower (model compilation)
- Use `--steps 50` for faster generation (lower quality)
- Use `--samples 1` to generate one model at a time

