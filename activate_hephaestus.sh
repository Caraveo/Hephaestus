#!/bin/bash
# Quick activation script for Hephaestus
# This ensures the OpenMP workaround is set

# Set OpenMP workaround
export KMP_DUPLICATE_LIB_OK=TRUE

# Activate conda environment
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate hephaestus

echo "✓ Hephaestus environment activated"
echo "✓ OpenMP workaround enabled (KMP_DUPLICATE_LIB_OK=TRUE)"
echo ""
echo "You can now run:"
echo "  python test_mps.py"
echo "  python -u sample_stage1.py --text 'a robot' --samples 1 --sampler ddim --steps 200 --cfg_scale 7.5 --seed 0"

