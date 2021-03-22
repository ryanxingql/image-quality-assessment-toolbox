# Image Quality Assessment Toolbox

- [Image Quality Assessment Toolbox](#image-quality-assessment-toolbox)
  - [Content](#content)
  - [Command](#command)
  - [Licenses](#licenses)

Feel free to contact: <ryanxingql@gmail.com>.

## Content

|metric|platform|class|range|better|note|ref|
|:-|:-|:-|:-|:-|:-|:-|
|peak signal-to-noise ratio (PSNR)|MATLAB|FR|[0, inf)|$\uparrow$|higher PSNR corresponds to lower mean squared error (MSE). when error at each pixel is MAX, PSNR equals to 0.|[[WIKI]](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio)|
|structural similarity index measure (SSIM)|MATLAB|FR|(?, 1]|$\uparrow$|difference between luminances (mean values), contrasts (variances) and structures (covariances) of two image patches.|[[WIKI]](https://en.wikipedia.org/wiki/Structural_similarity)|
|natural image quality evaluator (NIQE)|MATLAB|NR|[0, ?)|$\downarrow$|Mahalanobis distance between two multivariate Gaussian models of 36-dim features from natural (training) and input sharp patches.|[[MATLAB]](https://www.mathworks.com/help/images/ref/niqe.html) [[paper]](https://ieeexplore.ieee.org/document/6353522)|
|Ma *et al.* (MA)|MATLAB|NR|[0, 10]|$\uparrow$|joint difference in DCT, wavelet and PCA domains. very slow!|[[official repo]](https://github.com/chaoma99/sr-metric) [[paper]](https://arxiv.org/abs/1612.05890)|
|perceptual index (PI)|MATLAB|NR|[0, ?)|$\downarrow$|0.5 * ((10 - MA) + NIQE). very slow due to MA!|[[official repo]](https://github.com/roimehrez/PIRM2018) [[paper]](https://arxiv.org/abs/1809.07517)|
|learned perceptual image patch similarity (LPIPS)|PYTORCH|FR|[0, ?)|$\downarrow$|L2 distance between AlexNet/SqueezeNet/VGG activations of reference and distorted images; Trainable.|[[official repo]](https://github.com/richzhang/PerceptualSimilarity)|
|Fréchet inception distance (FID)|PYTORCH|FR|[0, ?)|$\downarrow$|Wasserstein-2 distance between two vectors of InceptionV3 activations (fed with reference and distorted images)|[[official repo]](https://github.com/mseitzer/pytorch-fid) [[paper]](https://arxiv.org/abs/1706.08500)|
|mean opinion score (MOS)|human|sub.|[0, 100]|$\uparrow$|image rating under strict rules and environment|[[BT.500]](https://www.itu.int/rec/R-REC-BT.500/)|
|degradation/difference/differential MOS (DMOS)|human|sub.|[0, 100]|$\downarrow$|difference between MOS values of reference and distorted images.|[[src1]](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=762345)  [[src2]](https://videoclarity.com/PDF/WPUnderstandingJNDMOSPSNR.pdf)|

## Command

<details>
<summary><b>Evaluate PSNR, SSIM and NIQE (MATLAB version)</b></summary>
<p>

1. Edit paths in `iqa_psnr_ssim_niqe.m`.
2. Run `iqa_psnr_ssim_niqe.m`.

Note that the list of the evaluated images is based on `dst_dir`.

</p>
</details>

<details>
<summary><b>Evaluate PI, NIQE (PIRM 18' version) and MA</b></summary>
<p>

1. Download `iqa_pi_niqe_ma` folder at [[百度网盘 (iqaa)]](https://pan.baidu.com/s/1jJB7EjdhPchGJ6XFKxF6IA).
2. Edit paths in `iqa_pi_niqe_ma.m`.
3. Run `iqa_pi_niqe_ma.m`.

Note that:

- the list of the evaluated images is based on `dst_dir`.
- the NIQE model (PIRM 18' version) is different from the MATLAB version (so as the results).

</p>
</details>

<details>
<summary><b>Evaluate LPIPS</b></summary>
<p>

1. Create CONDA environment: `conda create -n iqa python=3.7 -y`, and enter this environment: `conda activate iqa`.
2. Install TORCH: `python -m pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html`.
3. Install other dependecies: `python -m pip install opencv-python scipy tqdm`
4. Install LPIPS: `python -m pip install lpips=0.1.3`
5. Edit paths in `iqa_lpips.py`.
6. Run `iqa_lpips.py`.

Note that the list of the evaluated images is based on `dst_dir`.

</p>
</details>

<details>
<summary><b>Evaluate FID</b></summary>
<p>

1. Create CONDA environment: `conda create -n iqa python=3.7 -y`, and enter this environment: `conda activate iqa`.
2. Install packages: `pip install pytorch-fid==0.2.0`.
3. Edit paths in `iqa_fid.py`.
4. Run `iqa_fid.py`.

Note that the list of the evaluated images is based on `dst_dir`.

</p>
</details>

## Licenses

Please refer to the official repositories.
