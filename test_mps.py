#!/usr/bin/env python
"""Test script to verify MPS support and float16 compatibility."""
import torch
import sys
from utility.device_utils import get_device, get_dtype

def test_mps():
    """Test MPS availability and basic operations."""
    print("=" * 60)
    print("Hephaestus MPS Compatibility Test")
    print("=" * 60)
    
    # Check PyTorch version
    print(f"\nPyTorch version: {torch.__version__}")
    
    # Check CUDA
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")
    
    # Check MPS
    mps_available = False
    mps_built = False
    if hasattr(torch.backends, 'mps'):
        mps_built = torch.backends.mps.is_built()
        mps_available = torch.backends.mps.is_available()
    
    print(f"MPS built: {mps_built}")
    print(f"MPS available: {mps_available}")
    
    # Get device
    device = get_device(prefer_mps=True)
    dtype = get_dtype(device)
    
    print(f"\nSelected device: {device}")
    print(f"Selected dtype: {dtype}")
    
    # Test basic tensor operations
    print("\n" + "-" * 60)
    print("Testing basic tensor operations...")
    print("-" * 60)
    
    try:
        # Create a test tensor
        test_tensor = torch.randn(2, 3, 4).to(device)
        print(f"✓ Created tensor on {device}: {test_tensor.shape}, dtype: {test_tensor.dtype}")
        
        # Test float16 conversion if MPS
        if device.type == "mps":
            test_tensor_half = test_tensor.half()
            print(f"✓ Converted to float16: {test_tensor_half.dtype}")
            
            # Test basic operations with float16
            result = torch.matmul(test_tensor_half, test_tensor_half.transpose(-1, -2))
            print(f"✓ Matrix multiplication with float16: {result.shape}, dtype: {result.dtype}")
            
            # Test more complex operation
            result2 = torch.nn.functional.relu(result)
            print(f"✓ ReLU operation: {result2.shape}, dtype: {result2.dtype}")
        
        print("\n" + "=" * 60)
        print("✓ All tests passed! MPS setup is working correctly.")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 60)
        print("✗ Tests failed. Please check your setup.")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = test_mps()
    sys.exit(0 if success else 1)

