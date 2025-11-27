"""Device utilities for Mac MPS support with float16."""
import torch

def get_device(prefer_mps=True):
    """
    Get the best available device, preferring MPS on Mac.
    
    Args:
        prefer_mps: If True, prefer MPS over CPU on Mac
        
    Returns:
        torch.device: The device to use
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif prefer_mps and hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")

def get_dtype(device=None):
    """
    Get the appropriate dtype for the device.
    For MPS, use float16. For CUDA/CPU, use float32.
    
    Args:
        device: torch.device or None (will auto-detect)
        
    Returns:
        torch.dtype: The dtype to use
    """
    if device is None:
        device = get_device()
    
    if device.type == "mps":
        return torch.float16
    elif device.type == "cuda":
        # CUDA can use float16 too, but keeping float32 for compatibility
        return torch.float32
    else:
        return torch.float32

def empty_cache(device=None):
    """
    Empty the cache for the given device.
    Device-agnostic version of torch.cuda.empty_cache()
    
    Args:
        device: torch.device or None (will auto-detect)
    """
    if device is None:
        device = get_device()
    
    if device.type == "cuda":
        torch.cuda.empty_cache()
    elif device.type == "mps":
        torch.mps.empty_cache()

def to_device(tensor_or_module, device=None, dtype=None):
    """
    Move tensor or module to device with optional dtype conversion.
    
    Args:
        tensor_or_module: torch.Tensor or torch.nn.Module
        device: torch.device or None (will auto-detect)
        dtype: torch.dtype or None (will auto-detect based on device)
        
    Returns:
        Tensor or Module moved to device
    """
    if device is None:
        device = get_device()
    
    if dtype is None:
        dtype = get_dtype(device)
    
    # For modules, move to device first
    if isinstance(tensor_or_module, torch.nn.Module):
        result = tensor_or_module.to(device)
        # Don't convert module to half here - do it explicitly with .half() if needed
        return result
    
    # For tensors, move to device and optionally convert dtype
    result = tensor_or_module.to(device)
    
    # For MPS, convert to float16 if dtype is float16
    if device.type == "mps" and dtype == torch.float16:
        if result.dtype in [torch.float32, torch.float64]:
            result = result.to(dtype)
    
    return result

