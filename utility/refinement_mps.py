"""Mac MPS-compatible mesh refinement using Hephaestus model."""
import os
import torch
import numpy as np
import trimesh
import mcubes
from pathlib import Path
from tqdm import tqdm

from utility.device_utils import get_device, empty_cache
from utility.triplane_renderer.eg3d_renderer import sample_from_planes, generate_planes


def refine_mesh_mps(
    model,
    mesh_path,
    prompt,
    refinement_steps=200,
    mcubes_res=256,
    cfg_scale=7.5,
    sampler='ddim',
    outdir=None,
    save_name=None,
    verbose=True
):
    """
    Refine a mesh using iterative diffusion refinement (Mac MPS compatible).
    
    This method re-generates the model with higher quality settings to improve
    the mesh quality. Works on Mac MPS with float32.
    
    Args:
        model: The loaded Hephaestus diffusion model
        mesh_path: Path to input PLY mesh
        prompt: Text prompt for refinement
        refinement_steps: Number of diffusion steps (more = better quality, slower)
        mcubes_res: Marching cubes resolution (higher = more detail)
        cfg_scale: Classifier-free guidance scale
        sampler: Sampler type ('ddim', 'plms', 'dpm_solver')
        outdir: Output directory
        save_name: Output filename (without extension)
        verbose: Print progress
    
    Returns:
        Path to refined PLY file, or None if refinement failed
    """
    device = get_device(prefer_mps=True)
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"🔨 Starting MPS-compatible refinement (Mac)")
        print(f"   Device: {device}")
        print(f"   Refinement steps: {refinement_steps}")
        print(f"   Marching cubes resolution: {mcubes_res}")
        print(f"{'='*60}\n")
    
    try:
        # Load the sampler
        from ldm.models.diffusion.ddim import DDIMSampler
        from ldm.models.diffusion.plms import PLMSSampler
        from ldm.models.diffusion.dpm_solver import DPMSolverSampler
        
        if sampler == 'ddim':
            sampler_obj = DDIMSampler(model)
        elif sampler == 'plms':
            sampler_obj = PLMSSampler(model)
        elif sampler == 'dpm_solver':
            sampler_obj = DPMSolverSampler(model)
        else:
            raise ValueError(f"Unknown sampler: {sampler}")
        
        # Get text embedding
        if hasattr(model, 'cond_stage_model') and model.cond_stage_model is not None:
            with torch.no_grad():
                cond = model.get_learned_conditioning([prompt])
                unconditional_c = torch.zeros_like(cond)
        else:
            raise ValueError("Model does not have a condition stage model")
        
        # Sample with higher quality settings
        if verbose:
            print(f"Generating refined latent with {refinement_steps} steps...")
        
        shape = [8, 32, 96]  # Latent shape
        batch_size = 1
        samples, _ = sampler_obj.sample(
            S=refinement_steps,
            batch_size=batch_size,
            shape=shape,
            verbose=False,
            x_T=None,
            conditioning=cond.repeat(batch_size, 1, 1),
            unconditional_guidance_scale=cfg_scale,
            unconditional_conditioning=unconditional_c.repeat(batch_size, 1, 1),
            eta=0.0
        )
        
        # Decode to triplane
        if verbose:
            print("Decoding to triplane representation...")
        
        with torch.no_grad():
            decode_res = model.decode_first_stage(samples)
            decode_res = decode_res[0]  # Remove batch dimension
        
        # Extract mesh with higher resolution
        if verbose:
            print(f"Extracting mesh at {mcubes_res}x{mcubes_res}x{mcubes_res} resolution...")
        
        refined_ply_path = extract_mesh_high_res(
            model,
            decode_res,
            prompt,
            mcubes_res=mcubes_res,
            outdir=outdir,
            save_name=save_name,
            verbose=verbose
        )
        
        empty_cache(device)
        
        if refined_ply_path and os.path.exists(refined_ply_path):
            if verbose:
                print(f"\n{'='*60}")
                print(f"✓ MPS refinement complete!")
                print(f"  Refined mesh: {refined_ply_path}")
                print(f"{'='*60}\n")
            return refined_ply_path
        else:
            print("⚠ Warning: Mesh extraction failed")
            return None
            
    except Exception as e:
        print(f"⚠ Warning: MPS refinement failed: {e}")
        import traceback
        if verbose:
            traceback.print_exc()
        return None


def extract_mesh_high_res(
    model,
    decode_res,
    prompt,
    mcubes_res=256,
    outdir=None,
    save_name=None,
    verbose=True
):
    """
    Extract high-resolution mesh from triplane representation.
    
    Args:
        model: The loaded model
        decode_res: Decoded triplane tensor
        prompt: Text prompt
        mcubes_res: Resolution for marching cubes
        outdir: Output directory
        save_name: Output filename
    
    Returns:
        Path to extracted PLY file
    """
    device = get_device(prefer_mps=True)
    
    # Set output path
    if outdir is None:
        outdir = 'results/refined'
    os.makedirs(outdir, exist_ok=True)
    
    if save_name is None:
        save_name = prompt.replace(' ', '_') + '_refined'
    
    ply_path = os.path.join(outdir, f"{save_name}.ply")
    
    # Prepare volume for marching cubes
    c_list = torch.linspace(-1.2, 1.2, steps=mcubes_res, dtype=torch.float32)
    grid_x, grid_y, grid_z = torch.meshgrid(
        c_list, c_list, c_list, indexing='ij'
    )
    coords = torch.stack([grid_x, grid_y, grid_z], -1).to(device)
    
    # Sample features from triplane
    plane_axes = generate_planes()
    feats = sample_from_planes(
        plane_axes,
        decode_res.reshape(1, 3, -1, decode_res.shape[-2], decode_res.shape[-1]),
        coords.reshape(1, -1, 3),
        padding_mode='zeros',
        box_warp=2.4
    )
    
    # Get density
    fake_dirs = torch.zeros_like(coords).to(device)
    fake_dirs[..., 0] = 1
    
    with torch.no_grad():
        out = model.first_stage_model.triplane_decoder.decoder(
            feats,
            fake_dirs.reshape(1, -1, 3)
        )
    
    u = out['sigma'].reshape(mcubes_res, mcubes_res, mcubes_res).detach().cpu().numpy()
    del out, feats, coords
    empty_cache(device)
    
    # Marching cubes
    if verbose:
        print(f"Running marching cubes at {mcubes_res}³ resolution...")
    
    vertices, triangles = mcubes.marching_cubes(u, 10)
    
    # Normalize vertices to [-1.2, 1.2] range
    min_bound = np.array([-1.2, -1.2, -1.2], dtype=np.float32)
    max_bound = np.array([1.2, 1.2, 1.2], dtype=np.float32)
    vertices = vertices / (mcubes_res - 1) * (max_bound - min_bound)[None, :] + min_bound[None, :]
    
    # Extract vertex colors
    pt_vertices = torch.from_numpy(vertices.astype(np.float32)).to(device)
    
    # Render from multiple views to get colors
    res_triplane = 256
    render_kwargs = {
        'depth_resolution': 128,
        'disparity_space_sampling': False,
        'box_warp': 2.4,
        'depth_resolution_importance': 128,
        'clamp_mode': 'softplus',
        'white_back': True,
        'det': True
    }
    
    rays_o_list = [
        np.array([0, 0, 2], dtype=np.float32),
        np.array([0, 0, -2], dtype=np.float32),
        np.array([0, 2, 0], dtype=np.float32),
        np.array([0, -2, 0], dtype=np.float32),
        np.array([2, 0, 0], dtype=np.float32),
        np.array([-2, 0, 0], dtype=np.float32),
    ]
    
    rgb_final = None
    diff_final = None
    
    if verbose:
        print("Extracting vertex colors from multiple views...")
    
    for rays_o in tqdm(rays_o_list, disable=not verbose):
        rays_o_tensor = torch.from_numpy(rays_o.reshape(1, 3)).repeat(
            vertices.shape[0], 1
        ).float().to(device)
        rays_d = pt_vertices.reshape(-1, 3) - rays_o_tensor
        rays_d = rays_d / torch.norm(rays_d, dim=-1).reshape(-1, 1)
        dist = torch.norm(pt_vertices.reshape(-1, 3) - rays_o_tensor, dim=-1).cpu().numpy().reshape(-1)
        
        with torch.no_grad():
            render_out = model.first_stage_model.triplane_decoder(
                decode_res.reshape(1, 3, -1, res_triplane, res_triplane),
                rays_o_tensor.unsqueeze(0),
                rays_d.unsqueeze(0),
                render_kwargs,
                whole_img=False,
                tvloss=False
            )
        
        rgb = render_out['rgb_marched'].reshape(-1, 3).detach().cpu().numpy()
        depth = render_out['depth_final'].reshape(-1).detach().cpu().numpy()
        depth_diff = np.abs(dist - depth)
        
        if rgb_final is None:
            rgb_final = rgb.copy()
            diff_final = depth_diff.copy()
        else:
            ind = diff_final > depth_diff
            rgb_final[ind] = rgb[ind]
            diff_final[ind] = depth_diff[ind]
        
        del render_out
        empty_cache(device)
    
    # BGR to RGB
    rgb_final = np.stack([
        rgb_final[:, 2], rgb_final[:, 1], rgb_final[:, 0]
    ], -1)
    
    # Export to PLY
    mesh = trimesh.Trimesh(
        vertices,
        triangles,
        vertex_colors=(rgb_final * 255).astype(np.uint8)
    )
    trimesh.exchange.export.export_mesh(mesh, ply_path, file_type='ply')
    
    return ply_path


def refine_mesh_automatic_mps(
    model,
    ply_path,
    prompt,
    high_quality=True,
    outdir=None
):
    """
    Automatically refine a mesh with optimal MPS settings.
    
    Args:
        model: The loaded Hephaestus model
        ply_path: Path to input PLY mesh
        prompt: Text prompt
        high_quality: Use high quality settings (more steps, higher resolution)
        outdir: Output directory
    
    Returns:
        Path to refined PLY file
    """
    if outdir is None:
        outdir = str(Path(ply_path).parent)
    
    # High quality: 200 steps, 256 resolution
    # Standard: 100 steps, 128 resolution
    refinement_steps = 200 if high_quality else 100
    mcubes_res = 256 if high_quality else 128
    
    save_name = Path(ply_path).stem + '_refined'
    
    return refine_mesh_mps(
        model=model,
        mesh_path=ply_path,
        prompt=prompt,
        refinement_steps=refinement_steps,
        mcubes_res=mcubes_res,
        cfg_scale=7.5,
        sampler='ddim',
        outdir=outdir,
        save_name=save_name,
        verbose=True
    )

