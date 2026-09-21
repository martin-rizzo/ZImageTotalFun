## {#WORKFLOW_NAME}

{#WORKFLOW_DESCRIPTION}

## Parameters

__seed__
* The initial number for random generation. Each unique seed produces a different image.
* Results in significantly more dramatic variations when __"turbo_creativity"__ is turned on.

__style__
* The visual style that defines the overall look of your final image.

__palette__
* The color palette to use. This acts as a guide and is not always strictly followed in the final generated image.

__imprint_style_label__
* Prints the name of the selected style directly onto the image.
* It is recommended to leave this disabled by default.

__prompt__
* The text description of what you want to see, including subjects, actions, and settings.
* Avoid style keywords such as photo, comic, or blur, as the selected styles handle all visual effects automatically.

__steps__
* The number of iterations performed during the denoising process.
* The optimal setting is 8 steps. Increase this value only if you require better quality or need to fix minor hallucinations caused by __"turbo_creativity"__, keeping in mind that higher step counts result in longer render times.

__initial_bias__
* Adjusts the starting noise deviation to correct color issues, brightness, or even weird hallucinations.
* 0.0 serves as the optimal setting and is generally best left unchanged due to its unpredictable effects.

__turbo_creativity__
* Shakes up the generation process to produce unique, original compositions and avoid generic AI aesthetics.
* It is prone to generating hallucinations and duplicate elements, especially in high-contrast images.
* Disable this feature if you require highly precise and complex images.
* Enable this feature when exploring creative compositions with substantial variations between different seeds.
* Working with __turbo_creativity__ involves testing multiple seeds until you find the ideal one.
* Some minor defects and small hallucinations can be corrected by tweaking __"steps"__ and __"initial_bias"__.
* Note that seed numbers that are multiples of 3 cause __turbo_creativity__ to hallucinate more frequently, as the sampler internally skips one correction step to maximize image variation.

__detailed_sampling__
* Applies a different sampling method during the final steps to add finer details, although it may increase the generation time.

__contrast__
* Controls how smooth or intense the brightness transitions appear in the final image.
* 0.0 serves as the neutral baseline.

__color__
* Adjusts the color saturation of the image.
* 0.0 serves as the neutral baseline.

__hue__
* Modifies the color tint, primarily used to calibrate skin tones.
* 0.0 serves as the neutral baseline.

__orientation__
* Sets the orientation of the final image, where vertical creates a portrait format and horizontal creates a landscape format.

__aspect_ratio__
* Determines the proportional relationship between the width and height of the final image.

__ck_attention__
* Enables Comfy-Kitchen attention to reduce generation time. This takes effect only in newer versions of ComfyUI that support this optimization.

__zimage_turbo_ckpt__
* The checkpoint file used for the Z-Image Turbo diffusion model.

__qwen3_4b_ckpt__
* The checkpoint file used as text encoder, which must be based on the Qwen3-4b model.

__vae__
* The checkpoint file used for the variational autoencoder.

## Created by Martin Rizzo
* GitHub : https://github.com/martin-rizzo
* CivitAI: https://civitai.com/user/Photographer
* Reddit : https://www.reddit.com/user/FotografoVirtual


