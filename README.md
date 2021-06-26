# Image Quality Assessment Toolbox

Current version: [v2]; archived version: [[v1]](https://github.com/RyanXingQL/Image-Quality-Assessment-Toolbox/tree/1067537dab42509ef4b3cbd55c66a326a1d8dc7a)

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
|Fréchet inception distance (FID)|FR|Wasserstein-2 distance between two vectors of InceptionV3 activations (fed with reference and distorted images).|lower|[0, ?)|[[cleanfid repo]](https://github.com/GaParmar/clean-fid/tree/ced1e5657d4d9a9cf79358445a0bfcc3bb4d44ff) [[paper]](https://arxiv.org/abs/1706.08500)|PYTORCH|
|mean opinion score (MOS)|sub.|Image rating under strict rules and environment.|higher|[0, 100]|[[BT.500]](https://www.itu.int/rec/R-REC-BT.500/)|human|
|degradation/difference/differential MOS (DMOS)|sub.|Difference between MOS values of reference and distorted images.|lower|[0, 100]|[[src1]](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=762345)  [[src2]](https://videoclarity.com/PDF/WPUnderstandingJNDMOSPSNR.pdf)|human|

## 2. Evaluation

### 2.1. Notation

- src: source, e.g., raw images.
- dst: distorted, e.g., jpeg-compressed images.
- tar: target, e.g., enhanced compressed images.

### 2.2. Dependency

#### Basis

```bash
conda create -n iqa python=3.7 -y && conda activate iqa
python -m pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html
python -m pip install opencv-python scipy tqdm
```

```bash
# for iqa
python -m pip install lpips==0.1.3

# for fid
python -m pip install requests==2.25.1
```

For `iqa_pi_niqe_ma.m`, download `src.zip` at [Releases](https://github.com/RyanXingQL/Image-Quality-Assessment-Toolbox/releases), and unzip it as `./iqa_pi_niqe_ma/src/`.

#### All in one

You can run all the scripts (including MATLAB scripts) in one Python script `main.py`. We first need YAML support:

```bash
python -m pip install pyyaml
```

To run MATLAB by Python, we also need MATLAB IO in Python. Check [here](https://www.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-engine-for-python.html). My solution:

```bash
# linux
cd "matlabroot/extern/engines/python"  # e.g., ~/Matlab/R2019b/extern/engines/python
conda activate iqa && python setup.py install
```

### 2.3. Run

1. Edit `opt.yml`.
2. Run: `conda activate iqa && CUDA_VISIBLE_DEVICES=0 python main.py -case div2k_qf10 [-opt opt.yml -mode a -if_src true -if_dst true -start_idx 0 -max_num -1]`.

You can also run all the IQA scripts separately.

### 2.4. Note

- The list of the evaluated images is based on `tar_dir`.
- The NIQE model (PIRM 18' version, denoted by NIQE) is different from the MATLAB built-in version (denoted by NIQE-M); so as the results. We evaluate both of them.
- We do not evaluate the FID score between two images, but two folders of images instead. Therefore, FID returns only one score for all images. Check [here](https://github.com/RyanXingQL/Image-Quality-Assessment-Toolbox/wiki/Do-Not-Evaluate-FID-between-Two-Images).

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
