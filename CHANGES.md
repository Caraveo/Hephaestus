# Changes for Mac MPS Support (Hephaestus)

## Summary

This repository has been adapted to run on macOS using Metal Performance Shaders (MPS) with float16 precision. The project is now named "Hephaestus" while maintaining compatibility with the original 3DTopia codebase.

## Key Changes

### 1. Device Management (`utility/device_utils.py`)
- New utility module for device-agnostic operations
- Automatic MPS detection and preference
- Float16 support for MPS devices
- Device-agnostic memory management

### 2. Environment Configuration (`environment_mac.yml`)
- Mac-compatible conda environment
- Removed CUDA-specific dependencies
- Added PyTorch with MPS support
- Compatible with Python 3.10+

### 3. Updated Scripts
- `sample_stage1.py`: Full MPS support with float16
- `gradio_demo.py`: MPS support, optional threefiner dependency
- All diffusion samplers (DDIM, PLMS, DPM): Device-agnostic

### 4. Fixed Hardcoded CUDA References
- `ldm/models/diffusion/ddim.py`: Device-agnostic buffer registration
- `ldm/models/diffusion/plms.py`: Device-agnostic buffer registration
- `ldm/models/diffusion/dpm_solver/sampler.py`: Device-agnostic buffer registration
- `module/quantize_taming.py`: Removed hardcoded device initialization
- Replaced `torch.cuda.empty_cache()` with device-agnostic version

### 5. Documentation
- `README_MAC.md`: Comprehensive Mac setup guide
- `QUICKSTART_MAC.md`: Quick start guide
- Updated main `README.md` with Mac support information

### 6. Testing
- `test_mps.py`: Verification script for MPS setup

## Usage

See `QUICKSTART_MAC.md` for installation and usage instructions.

## Known Limitations

- Second stage refinement (threefiner) requires separate installation
- Some operations may fall back to CPU if not supported by MPS
- Maximum tensor sizes may differ on MPS vs CUDA

## Compatibility

- macOS 12.3+ (for MPS support)
- Apple Silicon (M1/M2/M3) or Intel Mac with Apple Silicon support
- Python 3.10+
- PyTorch 2.0.0+

