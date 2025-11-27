"""Threefiner refinement utilities for Hephaestus."""
import os
import sys
import subprocess
import trimesh
from pathlib import Path

def ply_to_glb(ply_path, glb_path=None):
    """
    Convert PLY mesh to GLB format for threefiner.
    
    Args:
        ply_path: Path to input PLY file
        glb_path: Path to output GLB file (optional, defaults to same name with .glb extension)
    
    Returns:
        Path to the created GLB file
    """
    if glb_path is None:
        glb_path = str(Path(ply_path).with_suffix('.glb'))
    
    try:
        mesh = trimesh.load(ply_path)
        mesh.export(glb_path, file_type='glb')
        print(f"✓ Converted {ply_path} to {glb_path}")
        return glb_path
    except Exception as e:
        print(f"⚠ Warning: Failed to convert PLY to GLB: {e}")
        return None

def check_threefiner_available():
    """Check if threefiner CLI is available."""
    try:
        result = subprocess.run(
            ['threefiner', '--help'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def check_cuda_available():
    """Check if CUDA is available (required for threefiner)."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False

def check_mps_available():
    """Check if MPS is available (for Mac refinement)."""
    try:
        import torch
        return hasattr(torch.backends, 'mps') and torch.backends.mps.is_available()
    except:
        return False

def refine_with_threefiner(
    mesh_path,
    prompt,
    refinement_mode='if2',
    outdir=None,
    save_name=None,
    iters=1000,
    front_dir='-y',
    text_dir=True,
    verbose=True
):
    """
    Refine a mesh using threefiner.
    
    Args:
        mesh_path: Path to input mesh (PLY or GLB)
        prompt: Text prompt for refinement
        refinement_mode: 'if2', 'sd', 'if', 'sd_fixgeo', 'if_fixgeo', 'if2_fixgeo'
        outdir: Output directory (defaults to same as input)
        save_name: Output filename (without extension)
        iters: Number of refinement iterations (default: 1000)
        front_dir: Front facing direction (default: '-y')
        text_dir: Use directional text prompt (default: True)
        verbose: Print verbose output (default: True)
    
    Returns:
        Path to refined GLB file, or None if refinement failed
    """
    # Check if threefiner is available
    if not check_threefiner_available():
        print("⚠ Warning: threefiner CLI not found. Skipping refinement.")
        print("  Install with: pip install threefiner")
        print("  Note: threefiner requires CUDA (Linux/Windows with NVIDIA GPU)")
        return None
    
    # Check if CUDA is available
    if not check_cuda_available():
        print("⚠ Warning: CUDA not available. threefiner requires CUDA.")
        print("  Refinement skipped. Generated mesh will be unrefined.")
        return None
    
    # Convert PLY to GLB if needed
    mesh_path_glb = mesh_path
    if mesh_path.endswith('.ply'):
        print(f"Converting {mesh_path} to GLB format for threefiner...")
        glb_path = ply_to_glb(mesh_path)
        if glb_path is None:
            return None
        mesh_path_glb = glb_path
    
    # Set output directory and filename
    if outdir is None:
        outdir = str(Path(mesh_path_glb).parent)
    else:
        os.makedirs(outdir, exist_ok=True)
    
    if save_name is None:
        save_name = Path(mesh_path_glb).stem + '_refined'
    
    # Build threefiner command
    cmd = [
        'threefiner', refinement_mode,
        '--mesh', mesh_path_glb,
        '--prompt', prompt,
        '--outdir', outdir,
        '--save', f'{save_name}.glb',
        '--iters', str(iters),
    ]
    
    if text_dir:
        cmd.extend(['--text_dir', '--front_dir', front_dir])
    
    if verbose:
        cmd_str = ' '.join(cmd)
        print(f"\n{'='*60}")
        print(f"🔨 Starting threefiner refinement...")
        print(f"Command: {cmd_str}")
        print(f"{'='*60}\n")
    
    try:
        # Run threefiner
        result = subprocess.run(
            cmd,
            capture_output=not verbose,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            refined_path = os.path.join(outdir, f'{save_name}.glb')
            if os.path.exists(refined_path):
                print(f"✓ Refinement complete! Saved to: {refined_path}")
                return refined_path
            else:
                print(f"⚠ Warning: Refinement completed but output file not found: {refined_path}")
                return None
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            print(f"⚠ Warning: threefiner refinement failed:")
            print(f"  {error_msg}")
            return None
            
    except Exception as e:
        print(f"⚠ Warning: Error running threefiner: {e}")
        return None

def refine_mesh_automatic(
    ply_path,
    prompt,
    high_quality=True,
    outdir=None
):
    """
    Automatically refine a mesh with optimal settings.
    
    Args:
        ply_path: Path to input PLY mesh
        prompt: Text prompt
        high_quality: Use high quality settings (more iterations)
        outdir: Output directory
    
    Returns:
        Path to refined GLB file, or None if refinement not available
    """
    if outdir is None:
        outdir = str(Path(ply_path).parent)
    
    # Two-stage refinement for best quality
    # Stage 1: SD refinement (if needed)
    # Stage 2: IF2 refinement (best quality)
    
    save_name_base = Path(ply_path).stem
    
    # Use IF2 directly for best quality (it handles both geometry and texture)
    refined_path = refine_with_threefiner(
        mesh_path=ply_path,
        prompt=prompt,
        refinement_mode='if2',
        outdir=outdir,
        save_name=save_name_base,
        iters=1000 if high_quality else 400,
        front_dir='-y',
        text_dir=True,
        verbose=True
    )
    
    return refined_path

