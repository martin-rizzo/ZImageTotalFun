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
3. [Checkpoints Used](#checkpoints-used)
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

## Checkpoints Used

Please ensure you update ComfyUI first and have the latest version of the Z-Image Power Nodes installed.

### diffusion_models

- __[z_image_turbo_int8_convrot_bf16emixed.safetensors](https://huggingface.co/martin-rizzo/Z-Image-Turbo-INT8-ConvRot-ComfyUI/resolve/main/z_image_turbo_int8_convrot_bf16emixed.safetensors)__ [6.17 GB]  
  Local: _`ComfyUI/models/diffusion_models/`__

### text_encoders

- __[qwen3-4b_int8_convrot_fp16emixed.safetensors](https://huggingface.co/martin-rizzo/Qwen3-4B-INT8-ConvRot-ComfyUI/resolve/main/qwen3-4b_int8_convrot_fp16emixed.safetensors)__ [4.42 GB]  
  Local: _`ComfyUI/models/text_encoders/`__

### vae

- __[Z-Image_half_natural_vae.safetensors](https://huggingface.co/easygoing0114/Z-Image_clear_vae/resolve/main/Z-Image_half_natural_vae.safetensors)__ [335 MB]  
  Local: _`ComfyUI/models/vae/`__

### Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   │
│   └── 📂 diffusion_models/
│   │   └── z_image_turbo_int8_convrot_bf16emixed.safetensors
│   │
│   ├── 📂 text_encoders/
│   │   └── qwen3-4b_int8_convrot_fp16emixed.safetensors
│   │
│   ├── 📂 vae/
│   │   └── Z-Image_half_natural_vae.safetensors
```

## Alternative Checkpoints

> The following checkpoints are provided as alternatives in case you experience issues.  
> Due to the wide variety of GPUs, VRAM capacities, and ComfyUI versions, one of these may work better for your system.

### diffusion_models

- __[z_image_turbo-Q5_K_S.gguf](https://huggingface.co/jayn7/Z-Image-Turbo-GGUF/resolve/main/z_image_turbo-Q5_K_S.gguf)__ [5.19 GB] : GGUF
- __[z_image_turbo_int8_convrot.safetensors](https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_int8_convrot.safetensors)__ [6.20 GB] : ComfyOrg I8ConvRot
- __[z_image_turbo_bf16.safetensors](https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors)__ [12.3 GB] : ComfyOrg BF16

### text_encoders

- __[Qwen3-4B-Q8_0.gguf](https://huggingface.co/Qwen/Qwen3-4B-GGUF/resolve/main/Qwen3-4B-Q8_0.gguf)__ [4.28 GB] : GGUF
- __[qwen_3_4b_fp8_mixed.safetensors](https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b_fp8_mixed.safetensors)__ [5.63 GB] : ComfyOrg FP8
- __[qwen_3_4b.safetensors](https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors)__ [8.04 GB] : ComfyOrg BF16

### vae

- __[ae.safetensors](https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors)__ [335 MB] : ComfyOrg
- More: [Z-Image_clear_vae](https://huggingface.co/easygoing0114/Z-Image_clear_vae), [Z-Image_Anime_VAE](https://huggingface.co/Anzhc/Z-Image_Anime_VAE)


## License

This project is licensed under the Creative Commons Zero v1.0 Universal (CC0 1.0)  
See the [LICENSE](LICENSE) file for details.

---

<div align="center">
⭐ If you like what you see, give the repository a star. Your support inspires more explorations!
</div>
