# Image Quality Assessment Toolbox

- [Image Quality Assessment Toolbox](#image-quality-assessment-toolbox)
  - [1. Content](#1-content)
  - [2. Command](#2-command)
    - [Evaluate PSNR, SSIM and NIQE (MATLAB built-in version)](#evaluate-psnr-ssim-and-niqe-matlab-built-in-version)
    - [Evaluate PI, NIQE (PIRM 18' version) and MA](#evaluate-pi-niqe-pirm-18-version-and-ma)
    - [Evaluate LPIPS](#evaluate-lpips)
    - [Evaluate FID](#evaluate-fid)
  - [3. Learn More](#3-learn-more)
  - [4. Licenses](#4-licenses)

Current version: [v1]

:e-mail: Feel free to contact: `ryanxingql@gmail.com`.

## 1. Content

|metric|class|note|better|range|ref|platform|
|:-|:-|:-|:-|:-|:-|:-|
|peak signal-to-noise ratio (PSNR)|FR|Higher PSNR corresponds to lower mean squared error (MSE). When error at each pixel is MAX, PSNR equals to 0.|higher|[0, inf)|[[WIKI]](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio)|MATLAB|
|structural similarity index measure (SSIM)|FR|Difference between luminances (mean values), contrasts (variances) and structures (covariances) of two image patches.|higher|(?, 1]|[[WIKI]](https://en.wikipedia.org/wiki/Structural_similarity)|MATLAB|
|natural image quality evaluator (NIQE)|NR|Mahalanobis distance between two multivariate Gaussian models of 36-dim features from natural (training) and input sharp patches.|lower|[0, ?)|[[MATLAB]](https://www.mathworks.com/help/images/ref/niqe.html) [[paper]](https://ieeexplore.ieee.org/document/6353522)|MATLAB|
|Ma *et al.* (MA)|NR|Joint difference in DCT, wavelet and PCA domains. Very slow!|higher|[0, 10]|[[official repo]](https://github.com/chaoma99/sr-metric) [[paper]](https://arxiv.org/abs/1612.05890)|MATLAB|
|perceptual index (PI)|NR|0.5 * ((10 - MA) + NIQE). Very slow due to MA!|lower|[0, ?)|[[official repo]](https://github.com/roimehrez/PIRM2018) [[paper]](https://arxiv.org/abs/1809.07517)|MATLAB|
|learned perceptual image patch similarity (LPIPS)|FR|L2 distance between AlexNet/SqueezeNet/VGG activations of reference and distorted images. trainable.|lower|[0, ?)|[[official repo]](https://github.com/richzhang/PerceptualSimilarity)|PYTORCH|
|Fréchet inception distance (FID)|FR|Wasserstein-2 distance between two vectors of InceptionV3 activations (fed with reference and distorted images).|lower|[0, ?)|[[official repo]](https://github.com/mseitzer/pytorch-fid) [[paper]](https://arxiv.org/abs/1706.08500)|PYTORCH|
|mean opinion score (MOS)|sub.|Image rating under strict rules and environment.|higher|[0, 100]|[[BT.500]](https://www.itu.int/rec/R-REC-BT.500/)|human|
|degradation/difference/differential MOS (DMOS)|sub.|Difference between MOS values of reference and distorted images.|lower|[0, 100]|[[src1]](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=762345)  [[src2]](https://videoclarity.com/PDF/WPUnderstandingJNDMOSPSNR.pdf)|human|

## 2. Command

Note:

- src: source, e.g., raw images; dst: distorted, e.g., jpeg-compressed images; tar: target, e.g., enhanced compressed images.
- the list of the evaluated images is based on `tar_dir`.

### Evaluate PSNR, SSIM and NIQE (MATLAB built-in version)

1. Edit paths in `iqa_psnr_ssim_niqe.m`.
2. Run `iqa_psnr_ssim_niqe.m`.

### Evaluate PI, NIQE (PIRM 18' version) and MA

1. Download `src.zip` at Releases. Unzip it as `./iqa_pi_niqe_ma/src/`.
2. Edit paths in `iqa_pi_niqe_ma.m`.
3. Run `iqa_pi_niqe_ma.m`.

Note: the NIQE model (PIRM 18' version) is different from the MATLAB built-in version (so as the results).

### Evaluate LPIPS

1. Create CONDA environment: `conda create -n iqa python=3.7 -y`, and enter this environment: `conda activate iqa`.
2. Install TORCH: `python -m pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html`.
3. Install other dependecies: `python -m pip install opencv-python scipy tqdm lpips==0.1.3`
4. Edit paths in `iqa_lpips.py`.
5. Run `iqa_lpips.py`.

### Evaluate FID

1. Create CONDA environment: `conda create -n iqa python=3.7 -y`, and enter this environment: `conda activate iqa`.
2. Install dependecies: `pip install pytorch-fid==0.2.0`.
3. Edit paths in `iqa_fid.py`.
4. Run `iqa_fid.py`.

## 3. Learn More

If you want to learn more about this repository, check [here](https://github.com/RyanXingQL/Image-Quality-Assessment-Toolbox/wiki).

## 4. Licenses

Please refer to the official repositories.

If you find this repository helpful, you may cite:

```tex
@misc{IQAT_xing_2021,
  author = {Qunliang Xing},
  title = {Image Quality Assessment Toolbox},
  howpublished = "\url{https://github.com/RyanXingQL/Image-Quality-Assessment-Toolbox}",
  year = {2021}, 
  note = "[Online; accessed 11-April-2021]"
}
```
