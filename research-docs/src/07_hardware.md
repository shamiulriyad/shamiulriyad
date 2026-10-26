# H. Hardware and software requirements

**All hardware figures in this section are estimates for planning. None was measured.** Measure memory and runtime with a short profiling run (Section I.6) before buying or booking hardware.

![Figure 5. Three hardware configurations (estimates, not measured minimums).](figures/fig5_hardware.svg){#fig:hardware width=100%}

## H.1 What drives memory and time

**Image arrays (calculation).** One float32 image of $H \times W$ pixels needs $4HW$ bytes:

- 4096×4096: 4 × 16,777,216 B ≈ 64 MiB.
- A group of 5 images keeps about 15 such arrays in memory (images, registered images, probabilities, weights, maps): about 1 GiB.
- At 8192×8192, each array is 256 MiB and 15 arrays are about 3.75 GiB. Tiling is then advisable.

**CNN training memory.** Activation memory grows roughly linearly with batch size × patch height × patch width × the summed channel widths of the network. Doubling the patch side therefore about quadruples activation memory. Mixed precision (fp16/bf16) roughly halves activation memory, and gradient checkpointing trades compute for memory. Model parameters and optimiser state (Adam keeps two extra copies) add about 4× the parameter memory. This is small for a U-Net (tens of millions of parameters ≈ hundreds of MB).

**PatchCore memory bank (calculation).** Memory = images × patches per image × feature dimension × 4 bytes. *Example:* 200 training images, a 28×28 feature grid (784 patches) and 1,024-dimensional features give 200 × 784 × 1,024 × 4 B ≈ 642 MB before subsampling. A 10% coreset gives about 64 MB, and 1% about 6.4 MB. The nearest-neighbour search cost scales with bank size.

**Dataset size.** This affects storage and epoch time, not peak memory, provided data is streamed from disk.

## H.2 Configurations

| | 1. CPU-only prototype | 2. Entry-level GPU development | 3. Research workstation |
|---|---|---|---|
| Purpose | Preprocessing, classical registration, fusion, small experiments | Supervised segmentation, PatchCore/PaDiM, modest reconstruction | High resolution, large sweeps, ensembles, optional diffusion |
| CPU | Modern x86-64 or ARM64, 4–8 cores | 8–16 cores | 16–32 cores |
| System RAM | 16 GB (32 GB for > 4k images) | 32 GB | 64–128 GB |
| GPU VRAM | None | **8–12 GB** (NVIDIA, CUDA-capable) | 16–24 GB; 40–48 GB+ for diffusion fine-tuning or very large tiles |
| Storage | SSD, 100–250 GB free | NVMe SSD, 1 TB | NVMe SSD 2–4 TB plus backup/NAS |
| OS | Linux, Windows or macOS | Ubuntu LTS recommended; Windows/WSL2 possible | Ubuntu LTS |
| CUDA | Not needed | NVIDIA driver compatible with the chosen PyTorch CUDA build | Same |
| Workload limits | Learned models only at toy scale; PatchCore feasible but slow on small images; no diffusion | Patch-based training (256–512 px); pretrained inpainting inference at moderate resolution; no large-scale generative training | Diffusion fine-tuning only of pretrained models; still no training from scratch |

**CUDA note.** PyTorch's official pip and conda builds bundle the CUDA runtime libraries, so the main system requirement is an NVIDIA driver new enough for the CUDA version of the chosen build. Select the build with the selector at pytorch.org [48] at project start, record it in the lock file, and do not mix system CUDA toolkits with bundled ones unless compiling custom extensions.

## H.3 Recommendations by task

| Task | Recommendation (estimate) |
|---|---|
| **Inference on one group of 4–5 images** (Stage 1) | CPU is sufficient. Registration and fusion are dominated by FFTs, warping and sorting 4–5 values per pixel. Use float32 and process tiles if an image exceeds about 4k × 4k on a 16 GB machine. |
| **Inference with learned evidence** (Stages 2–3) | A GPU with 8 GB is comfortable for U-Net or PatchCore inference on tiles; the CPU works but is slower. |
| **Model training** | 8–12 GB VRAM for U-Net on 256–512 px patches with mixed precision. Start with batch 8 at 256 px and adjust from measured peak memory. 16–24 GB allows larger patches or batches and ensembles. |
| **High-resolution / tiled processing** | Tile with overlap (e.g. 512 px tiles, 64 px overlap) and blend; register globally first, then fuse per tile. Keep provenance consistent across tiles. RAM, not VRAM, is the main limit for whole-image fusion. |
| **Optional diffusion / inpainting experiments** | Pretrained model inference: at least the entry GPU, preferably 16–24 GB. Fine-tuning: 24 GB or more. No training from scratch. Treat these as experiments with flagged outputs. |

## H.4 Software stack and reproducible environment

**Core (recommended).**

- Python 3.11 or 3.12
- NumPy, SciPy
- OpenCV (`opencv-python-headless`; SIFT is in the main package since OpenCV 4.4) [46]
- scikit-image (`phase_cross_correlation`, metrics) [47]
- PyTorch + torchvision [48]
- Albumentations (augmentation; installs `opencv-python-headless`, so do not also install `opencv-python`) [49]
- Matplotlib, pandas, PyYAML, tifffile, tqdm, psutil

**Optional.**

- Anomalib (PatchCore, PaDiM) [50]
- segmentation-models-pytorch (U-Net variants)
- timm (backbones)
- faiss-cpu (nearest-neighbour search)
- MLflow or TensorBoard (experiment tracking)
- pytest, pre-commit, ruff (quality)

**Version management.**

- Declare top-level packages with lower bounds in `requirements.in`.
- Compile an exact lock file (`uv pip compile` or `pip-tools`) and commit it.
- Record the PyTorch build (CPU or CUDA variant) and the GPU driver version in every experiment log.
- Optionally build a Docker image from the lock file for the GPU machines.
- Appendix N.3 gives step-by-step commands.
