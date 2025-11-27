<div align="center">

<picture>
  <img alt="Hephaestus Logo" src="Hephaestus.png" width="25%">
</picture>

# 🔨 Hephaestus

### *Forge 3D Models Natively on Your Mac*

**Transform words into three-dimensional reality. Powered by the divine craft of Hephaestus, brought to life through Apple's Metal Performance Shaders.**

![Status](https://img.shields.io/badge/status-active-success)
![macOS](https://img.shields.io/badge/macOS-12.3%2B-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=Hephaestus.Hephaestus)](https://github.com/caraveo/Hephaestus)

---

</div>

## The Forge of Hephaestus

In the pantheon of Greek mythology, **Hephaestus** was the master craftsman of the gods—the divine blacksmith whose forge burned deep within Mount Etna. Though cast out of Olympus for his imperfections, he transformed his exile into mastery. With hammer and anvil, he crafted not just weapons and armor, but living automatons, golden thrones, and wonders that defied imagination.

Hephaestus worked in fire and metal, shaping raw materials into creations of breathtaking complexity. From simple descriptions, he forged reality—each piece a testament to the power of craft and vision.

---

## Welcome to Hephaestus

**Hephaestus** brings this ancient craft to your Mac, harnessing the power of modern AI to forge 3D models from text descriptions. Built upon the foundation of [3DTopia](https://github.com/3DTopia/3DTopia), this project transforms simple prompts into fully-realized 3D objects—all running natively on your Mac using Apple's Metal Performance Shaders (MPS) with float16 precision.

### What Makes Hephaestus Special?

🔥 **Native Mac Performance** - Optimized for Apple Silicon with MPS acceleration  
⚡ **Rapid Generation** - Create 3D models in minutes, not hours  
🎨 **Two-Stage Refinement** - Quick candidates, then polished perfection  
🧠 **Diffusion-Powered** - State-of-the-art AI model architecture  
✨ **Float16 Precision** - Efficient memory usage without sacrificing quality  

Simply describe what you want, and watch as Hephaestus transforms your words into three-dimensional reality—just as the divine smith once forged wonders from raw description and raw material.

---

## Quick Start

### For Mac Users

Hephaestus is optimized for macOS with native Metal Performance Shaders support. Getting started is simple:

```bash
# Clone the repository
git clone https://github.com/caraveo/Hephaestus.git
cd Hephaestus

# Create and activate the environment
conda env create -f environment_mac.yml
conda activate hephaestus

# Verify your setup (should show MPS available)
python test_mps.py

# Forge your first 3D model
python -u sample_stage1.py --text "a majestic dragon statue" --samples 1 --sampler ddim --steps 200 --cfg_scale 7.5 --seed 0
```

Your creation will appear in `results/default/stage1/`—a mesh file ready for use in any 3D application.

**📖 Detailed Mac setup instructions:** See [README_MAC.md](README_MAC.md)  
**⚡ Quick start guide:** See [QUICKSTART_MAC.md](QUICKSTART_MAC.md)

### For Linux/Windows (CUDA)

```bash
conda env create -f environment.yml
conda activate hephaestus
python -u sample_stage1.py --text "a robot" --samples 1 --sampler ddim --steps 200 --cfg_scale 7.5 --seed 0
```

---

## The Forging Process

Hephaestus uses a two-stage approach, mirroring the divine craftsman's method of rough shaping followed by meticulous refinement:

### Stage 1: Rapid Prototyping
The diffusion model quickly generates candidate 3D models from your text prompt. Multiple variations are created in seconds, giving you options to choose from.

### Stage 2: Masterful Refinement *(Optional)*
Selected models can be refined using [threefiner](https://github.com/3DTopia/threefiner) for enhanced detail and quality—the final polish on a masterwork.

---

## Features

### 🎯 Command-Line Interface

Generate models directly from the terminal with full control over all parameters:

```bash
python -u sample_stage1.py \
  --text "a steampunk watch" \
  --samples 4 \
  --sampler ddim \
  --steps 200 \
  --cfg_scale 7.5 \
  --seed 42 \
  --mcubes_res 128 \
  --render_res 128
```

**Key Parameters:**
- `--text` - Your creative prompt describing the 3D object
- `--samples` - Number of variations to generate (1-4)
- `--steps` - Sampling steps (more = higher quality, slower)
- `--cfg_scale` - Guidance scale (higher = more adherence to prompt)
- `--mcubes_res` - Resolution for mesh extraction (lower = less memory)
- `--render_res` - Video rendering resolution

### 🌐 Web Interface (Gradio)

Launch an interactive web interface for easy model generation:

```bash
python gradio_demo.py
```

Then open your browser to the provided URL. Simply enter your prompt, adjust settings, and watch Hephaestus forge your creation.

### 🎨 Output Formats

- **`.ply`** - Point cloud format, ready for 3D editing
- **`.mp4`** - Multi-view rotation videos showing your model from all angles
- **`.glb`** - After stage 2 refinement (if using threefiner)

---

## Requirements

### Mac (Recommended)
- macOS 12.3 or later
- Apple Silicon (M1/M2/M3) or Intel Mac
- Python 3.10+
- Anaconda or Miniconda
- At least 16GB RAM recommended

### Linux/Windows
- CUDA-capable GPU
- Python 3.8+
- Anaconda or Miniconda

---

## Installation Details

### Automatic Checkpoint Download

Model checkpoints are automatically downloaded on first run from [HuggingFace](https://huggingface.co/hongfz16/3DTopia). For manual download:

```bash
# Model will be saved to checkpoints/
# Or download manually: model.safetensors from hongfz16/3DTopia
```

### Stage 2 Refinement (Optional)

To enable the refinement stage, install [threefiner](https://github.com/3DTopia/threefiner) separately. Stage 1 works perfectly on its own for most use cases.

---

## Examples

Watch as Hephaestus transforms simple descriptions into 3D reality:

```
"a majestic dragon statue"          → Ancient guardian brought to life
"a retro computer from the 1980s"   → Nostalgic technology recreated
"a futuristic spaceship"            → Science fiction made tangible
"a cute robot with big eyes"        → Character design in three dimensions
"a detailed pocket watch"           → Precision craftsmanship realized
```

Each creation is unique—just as Hephaestus never forged the same item twice.

---

## Performance Tips

### For Mac Users

- **First Run**: May be slower as Metal compiles the model (one-time cost)
- **Memory Management**: Reduce `--mcubes_res` if you encounter memory issues
- **Speed vs Quality**: Lower `--steps` (50-100) for faster generation, higher (200-500) for better quality
- **Float16**: Automatically enabled on MPS—more efficient memory usage

### Optimization

- Start with lower resolution (`--mcubes_res 64`) to test prompts quickly
- Use `--samples 1` to generate one model at a time
- Disable video with `--no_video` to speed up generation

---

## Troubleshooting

### OpenMP Error on Mac

If you encounter OpenMP library conflicts, the scripts automatically handle this. If issues persist:

```bash
export KMP_DUPLICATE_LIB_OK=TRUE
```

Or use our activation script: `source activate_hephaestus.sh`

### MPS Not Available

Ensure you have:
- macOS 12.3+
- PyTorch 2.0.0+ installed
- Apple Silicon Mac (or Intel with Metal support)

Check with: `python test_mps.py`

### Out of Memory

Reduce resolution parameters:
```bash
--mcubes_res 64 --render_res 64
```

---

## Architecture

Hephaestus is built on the powerful [3DTopia](https://arxiv.org/pdf/2403.02234.pdf) architecture:

- **Latent Diffusion Model** - Core generative engine
- **Triplane VAE** - 3D representation learning
- **EG3D Renderer** - High-quality neural rendering
- **CLIP Text Encoder** - Understanding your prompts

All optimized for Mac with native Metal Performance Shaders support.

---

## Citation

If you use Hephaestus in your research or projects, please cite the original 3DTopia paper:

```bibtex
@article{hong20243dtopia,
  title={3DTopia: Large Text-to-3D Generation Model with Hybrid Diffusion Priors},
  author={Hong, Fangzhou and Tang, Jiaxiang and Cao, Ziang and Shi, Min and Wu, Tong and Chen, Zhaoxi and Wang, Tengfei and Pan, Liang and Lin, Dahua and Liu, Ziwei},
  journal={arXiv preprint arXiv:2403.02234},
  year={2024}
}
```

---

## Acknowledgments

Hephaestus stands on the shoulders of giants:

- **[3DTopia](https://github.com/3DTopia/3DTopia)** - The foundation that makes it all possible
- **[EG3D](https://github.com/NVlabs/eg3d)** - Neural rendering architecture
- **[Stable Diffusion](https://github.com/CompVis/stable-diffusion)** - Diffusion model framework
- **[Objaverse](https://objaverse.allenai.org)** - Training dataset
- **The open-source community** - Making AI accessible to all

Like Hephaestus drawing inspiration from the fires of the earth, this project draws from the collective wisdom of researchers and developers worldwide.

---

## License

This project maintains the same license as 3DTopia. See [LICENSE](LICENSE) for details.

---

## The Forge Awaits

Just as Hephaestus once transformed raw materials into divine creations, you can now transform words into three-dimensional reality. The forge is ready. The tools are prepared. What will you create?

**Begin your journey:** Start with `python test_mps.py` to verify your setup, then forge your first model and discover what's possible when ancient craft meets modern AI.

---

<div align="center">

*"From chaos and fire, beauty emerges. From words and vision, reality takes form."*

**— The Way of Hephaestus**

</div>
