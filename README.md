<div align="center">
# Z-Image Total Fun<br><sub><sup><i>Exploring visual styles with pure creative joy</i></sup></sub>
[![Platform](https://img.shields.io/badge/platform%3A-ComfyUI-007BFF)](#)  
[![License](https://img.shields.io/github/license/aiman/ComfyUI-ZImageTotalFun?label=license%3A&color=28A745)](#)  
[![Version](https://img.shields.io/github/v/tag/aiman/ComfyUI-ZImageTotalFun?label=version%3A&color=D07250)](#)  
[![Last](https://img.shields.io/github/last-commit/aiman/ComfyUI-ZImageTotalFun?label=last%20commit%3A)](#)  
<img src="banner_total_fun.jpg" width="90%"></img>
</div>

**Z-Image Total Fun** is a collection of experimental workflows designed to test and enjoy visual styles and prompting techniques with [Z-Image Turbo](https://github.com/Tongyi-MAI/Z-Image). No LoRAs, no upscalers—just pure prompting, executed in the simplest way possible, thanks to **Z-Image Power Nodes v2.1.1+** and the magic of **Nodes 2.0** and **Sub-graphs** in ComfyUI.

> 🎉 **The result? TOTAL FUN!** 🤩

Each workflow groups 10+ preconfigured visual styles around a specific theme (Cinema, Anime, Photobooth, Sketch, Stop Motion). They are specifically designed to leverage ComfyUI's latest features while being organized to make image generation highly intuitive and user-friendly.

## Table of Contents
1. [Workflows](#workflows)
2. [Requirements](#requirements)
3. [Recommended Checkpoints](#recommended-checkpoints)
4. [Installation](#installation)
5. [Project Structure](#project-structure)
6. [License](#license)

## Workflows

| Workflow | Theme | Size | Date |
|----------|-------|------|------|
| [ZImageTotalFun__anime.json](ZImageTotalFun__anime.json) | 🎌 Anime | 112 KB | Sep 15 |
| [ZImageTotalFun__cinema.json](ZImageTotalFun__cinema.json) | 🎬 Cinema | 111 KB | Sep 15 |
| [ZImageTotalFun__photobooth.json](ZImageTotalFun__photobooth.json) | 📸 Photobooth | 77 KB | Sep 03 |
| [ZImageTotalFun__sketch.json](ZImageTotalFun__sketch.json) | ✏️ Sketch | 90 KB | Aug 29 |
| [ZImageTotalFun__stopmo.json](ZImageTotalFun__stopmo.json) | 🎞️ Stop Motion | 93 KB | Sep 06 |

Each `.json` file is a complete, ready-to-use workflow. Simply load it, pick a style, and let Z-Image Turbo do the rest. Styles are organized by theme so you can explore one category at a time without feeling overwhelmed.

## Requirements

- **ComfyUI:** v0.2.7 or higher
- **Z-Image Power Nodes:** v2.1.1 or higher
- **Hardware:** CUDA-capable GPU (recommended)

## Recommended Checkpoints

The following checkpoints are used in each workflow, but any Z-Image Turbo checkpoint should work well, including the original models from the ComfyUI repository.

### Safetensors (INT8-ConvRot) — *Recommended*
- __`z_image_turbo_int8_convrot_bf16emixed.safetensors`__ <sub>~6.17 GB</sub>  
  Local: _`ComfyUI/models/diffusion_models/`__
- __`qwen3-4b_int8_convrot_fp16emixed.safetensors`__ <sub>~4.42 GB</sub>  
  Local: _`ComfyUI/models/text_encoders/`__
- __`Z-Image_half_natural_vae.safetensors`__ <sub>~335 MB</sub>  
  Local: _`ComfyUI/models/vae/`__

### Alternatives
Versions in **GGUF (Q5/Q8)**, **FP8**, and **BF16 original** are also available through the official ComfyUI repository and HuggingFace. If your hardware doesn't perform optimally with ConvRot, try the alternatives that best suit your setup.

## Installation

### Manual Installation (Recommended)
1. Open your preferred terminal.
2. Navigate to your ComfyUI directory:
   ```bash
   cd <your_comfyui_directory>
   ```
3. Create a folder for the workflows (or use your preferred location):
   ```bash
   mkdir -p ComfyUI/user_defaults/workflows
   ```
4. Place the `.json` files into that folder:
   ```bash
   cp ZImageTotalFun__*.json ComfyUI/user_defaults/workflows/
   ```
5. Restart ComfyUI, go to the **Workflows** tab, and you'll see all 5 workflows ready to load.

> **Note:** Make sure you have the checkpoints and Power Nodes installed before generating.

## Project Structure

```
ComfyUI-ZImageTotalFun/
├── ZImageTotalFun__anime.json
├── ZImageTotalFun__cinema.json
├── ZImageTotalFun__photobooth.json
├── ZImageTotalFun__sketch.json
├── ZImageTotalFun__stopmo.json
├── README.md
└── .gitignore
```

## License

This project is licensed under the Creative Commons Zero v1.0 Universal (CC0 1.0)  
See the [LICENSE](LICENSE) file for details.

---

<div align="center">
⭐ If you like what you see, give the repository a star. Your support inspires more explorations!
</div>