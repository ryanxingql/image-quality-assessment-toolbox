# Image Quality Assessment Toolbox

- [Image Quality Assessment Toolbox](#image-quality-assessment-toolbox)
  - [Content](#content)
  - [Command](#command)
  - [Licenses](#licenses)

Feel free to contact: <ryanxingql@gmail.com>.

## Content

|Metric|Implementation|Note|Ref|
|:-|:-|:-|:-|
|PSNR (dB)|MATLAB|FR; [0, inf); Higher is better; Higher PSNR = lower MSE.|[[WIKI]](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio)|
|SSIM|MATLAB|FR; (-1, 1]; Higher is better.|[[WIKI]](https://en.wikipedia.org/wiki/Structural_similarity)|
|NIQE|MATLAB|NR; [0, ?); Lower is better; Mahalanobis distance of 36 natural-scene-statistics-based features (fit into multivariate Gaussian models) from natural (training) and input sharp patches.|[[MATLAB]](https://www.mathworks.com/help/images/ref/niqe.html) [[paper]](https://ieeexplore.ieee.org/document/6353522)|
|MA|MATLAB|NR; [0, 10]; Higher is better; Very slow!|[[official repo]](https://github.com/chaoma99/sr-metric) [[paper]](https://arxiv.org/abs/1612.05890)|
|PI|MATLAB|NR; [0, ?); Lower is better; 0.5 * ((10 - MA) + NIQE); Very slow due to MA!|[[official repo]](https://github.com/roimehrez/PIRM2018) [[paper]](https://arxiv.org/abs/1809.07517)|
|LPIPS|PYTHON|FR; [0, ?); Lower is better; L2 distance of CNN activations from reference and distorted images; Trainable.|[[official repo]](https://github.com/richzhang/PerceptualSimilarity)|
|MOS|human|Subjective.|
|DMOS|human|Subjective.|

## Command

<details>
<summary><b>Calculate PSNR, SSIM and NIQE (MATLAB version) with MATLAB</b></summary>
<p>

1. Change `csv_file_name`, `ref_dir`, `src_dir` and `dst_dir` in `iqa_psnr_ssim_niqe.m`.
2. Run `iqa_psnr_ssim_niqe.m`.

Note that image list is based on `dst_dir`.

</p>
</details>

<details>
<summary><b>Calculate PI, NIQE (PIRM 18' version) and MA with MATLAB</b></summary>
<p>

1. Download `iqa_pi_niqe_ma` folder at [[百度网盘 (iqaa)]](https://pan.baidu.com/s/1jJB7EjdhPchGJ6XFKxF6IA).
2. Change `csv_file_name`, `ref_dir`, `src_dir` and `dst_dir` in `iqa_pi_niqe_ma.m`.
3. Run `iqa_pi_niqe_ma.m`.

Note that:

- image list is based on `dst_dir`.
- the NIQE model (PIRM 18' version) is different from the MATLAB version (so as the results). I prefer the latter.

</p>
</details>

<details>
<summary><b>Calculate LPIPS with PYTHON</b></summary>
<p>

1. Create CONDA environment: `conda create -n iqa python=3.7 -y`, and enter this environment: `conda activate iqa`.
2. Install TORCH: `python -m pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html`.
3. Install other dependencies: `python -m pip install lpips opencv-python scipy tqdm`
4. Change `csv_file_name`, `ref_dir`, `src_dir` and `dst_dir` in `iqa_lpips.py`.
5. Run `iqa_lpips.py`.

Note that image list is based on `dst_dir`.

</p>
</details>

## Licenses

Please refer to the official repositories.
