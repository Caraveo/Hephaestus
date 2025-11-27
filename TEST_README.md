# Extensive Test Suite

This comprehensive test suite validates all features of Hephaestus, including all sampler algorithms, refinement modes, and configuration options.

## Quick Start

```bash
# Run all tests
python test_extensive.py

# Run with quick mode (faster, fewer steps)
# Edit test_extensive.py: set quick_test = True
python test_extensive.py
```

## Test Coverage

### 1. Basic Generation
- Tests default settings with standard prompt
- Validates core generation pipeline

### 2. Sampler Algorithms
Tests all available samplers:
- **DDIM** - Denoising Diffusion Implicit Models
- **PLMS** - Pseudo Linear Multistep
- **DPM Solver** - Diffusion Probabilistic Model Solver

### 3. CFG Scales
Tests different classifier-free guidance scales:
- 1.0 (low guidance)
- 3.0 (moderate)
- 7.5 (recommended)
- 10.0 (high guidance)

### 4. Step Counts
Tests different sampling step counts:
- Quick mode: 30, 50
- Full mode: 50, 100, 200

### 5. Mesh Resolutions
Tests different marching cubes resolutions:
- 64³ (low quality, fast)
- 128³ (balanced)
- 256³ (high quality, slow)

### 6. MPS Refinement (Mac)
- Tests native Mac MPS refinement
- Validates automatic refinement workflow
- Only runs if MPS is available

### 7. Refinement Modes (CUDA)
Tests all threefiner refinement modes (if CUDA available):
- **if2** - Deepfloyd-IF-II (best quality)
- **sd** - Stable Diffusion
- **if** - Deepfloyd-IF
- **if2_fixgeo** - IF2 with geometry fixing
- **sd_fixgeo** - SD with geometry fixing
- **if_fixgeo** - IF with geometry fixing

### 8. Edge Cases
- Very short prompts
- Long detailed prompts
- Minimum step counts
- Extreme CFG scales
- Error handling

## Configuration

Edit `TEST_CONFIG` in `test_extensive.py`:

```python
TEST_CONFIG = {
    "base_prompt": "a test robot",
    "test_dir": "test_results",
    "quick_test": False,  # Set to True for faster tests
    "skip_refinement": False,  # Skip refinement tests
}
```

## Test Report

After running, a detailed JSON report is generated in `test_results/test_report.json` with:
- Test results for each case
- Success/failure status
- Duration for each test
- Error messages for failures
- Overall statistics

## Expected Duration

- **Quick mode**: ~10-15 minutes
- **Full mode**: ~1-2 hours (depending on hardware)

## Requirements

- Hephaestus environment activated
- Sufficient disk space for test outputs
- Python 3.10+
- For refinement tests: CUDA (Linux/Windows) or MPS (Mac)

## Troubleshooting

- **Timeouts**: Increase timeout values in test functions
- **Memory issues**: Reduce mesh resolutions in tests
- **Skip tests**: Set `skip_refinement = True` to skip refinement tests
- **Quick tests**: Set `quick_test = True` for faster validation

