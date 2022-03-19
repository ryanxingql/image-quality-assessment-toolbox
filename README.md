# Image Quality Assessment Toolbox

<img src="https://user-images.githubusercontent.com/34084019/124798339-cf824e80-df85-11eb-948f-c0612834c404.gif" width="70%">

:e-mail: Feel free to contact: `ryanxingql@gmail.com`.

## 0. Archive

- v3: add MS-SSIM index, BRISQUE and PIQE; re-implement PSNR and SSIM over Python; remove Ma _et al._ and PI due to the low computation efficiency; remove FID since it is not an image quality evaluator.
- [v2](https://github.com/ryanxingql/image-quality-assessment-toolbox/tree/d2f5e9dedd1b7bc0624142b67dbd0eee575b15e8): unify all scripts of algorithms.
- [v1](https://github.com/ryanxingql/image-quality-assessment-toolbox/tree/1067537dab42509ef4b3cbd55c66a326a1d8dc7a): the first formal version.

## 1. Content

|metric|class|description|better|range|ref|
|:-|:-|:-|:-|:-|:-|
|Peak signal-to-noise ratio (PSNR)|FR|The ratio of the maximum pixel intensity to the power of the distortion.|higher|`[0, inf)`|[[WIKI]](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio)|
|Structural similarity (SSIM) index|FR|Local similarity of luminance, contrast and structure of two image.|higher|`(?, 1]`|[[paper]](https://ieeexplore.ieee.org/document/1284395) [[WIKI]](https://en.wikipedia.org/wiki/Structural_similarity)|
|Multi-scale structural similarity (MS-SSIM) index|FR|Based on SSIM; combine luminance information at the highest resolution level with structure and contrast information at several down-sampled resolutions, or scales.|higher|`(?, 1]`|[[paper]](https://ieeexplore.ieee.org/document/1292216) [[code]](https://github.com/VainF/pytorch-msssim)|
|Learned perceptual image patch similarity (LPIPS)|FR|Obtain L2 distance between AlexNet/SqueezeNet/VGG activations of reference and distorted images; train a predictor to learn the mapping from the distance to similarity score. Trainable.|lower|`[0, ?)`|[[paper]](https://arxiv.org/abs/1801.03924) [[official repo]](https://github.com/richzhang/PerceptualSimilarity)|
|Blind/referenceless image spatial quality evaluator (BRISQUE)|NR|Model Gaussian distributions of mean subtracted contrast normalized (MSCN) features; obtain 36-dim Gaussian parameters; train an SVM to learn the mapping from feature space to quality score.|lower|`[0, ?)`|[[paper]](https://ieeexplore.ieee.org/document/6272356)|
|Natural image quality evaluator (NIQE)|NR|Mahalanobis distance between two multi-variate Gaussian models of 36-dim features from natural (training) and input sharp patches.|lower|`[0, ?)`|[[paper]](https://ieeexplore.ieee.org/document/6353522)|
|Perception based image quality evaluator (PIQE)|NR|Similar to NIQE; block-wise. PIQE is less computationally efficient than NIQE, but it provides local measures of quality in addition to a global quality score.|lower|`[0, 100]`|[[paper]](https://ieeexplore.ieee.org/document/7084843)|

Notations:

- FR: Full-reference quality metric.
- NR: No-reference quality metric.

Archived:

|metric|class|description|better|range|ref|where|
|:-|:-|:-|:-|:-|:-|:-|
|Ma *et al.* (MA)|NR|Extract features in DCT, wavelet and PCA domains; train a regression forest to learn the mapping from feature space to quality score. Very slow!|higher|`[0, 10]`|[[paper]](https://arxiv.org/abs/1612.05890) [[official repo]](https://github.com/chaoma99/sr-metric)|[[v2]](https://github.com/ryanxingql/image-quality-assessment-toolbox/tree/d2f5e9dedd1b7bc0624142b67dbd0eee575b15e8)|
|perceptual index (PI)|NR|0.5 * ((10 - MA) + NIQE). Very slow due to MA!|lower|`[0, ?)`|[[paper]](https://arxiv.org/abs/1809.07517) [[official repo]](https://github.com/roimehrez/PIRM2018)|[[v2]](https://github.com/ryanxingql/image-quality-assessment-toolbox/tree/d2f5e9dedd1b7bc0624142b67dbd0eee575b15e8)|
|Fréchet inception distance (FID)|FR|Wasserstein-2 distance between two Gaussian models of InceptionV3 activations (fed with reference and distorted image data-sets, respectively).|lower|`[0, ?)`|[[paper]](https://arxiv.org/abs/1706.08500) [[cleanfid repo]](https://github.com/GaParmar/clean-fid/tree/ced1e5657d4d9a9cf79358445a0bfcc3bb4d44ff)|[[v2]](https://github.com/ryanxingql/image-quality-assessment-toolbox/tree/d2f5e9dedd1b7bc0624142b67dbd0eee575b15e8)|

Subjective quality metric(s):

|metric|description|better|range|ref|
|:-|:-|:-|:-|:-|
|mean opinion score (MOS)|Image rating under certain standards.|higher|`[0, 100]`|[[BT.500]](https://www.itu.int/rec/R-REC-BT.500/)|
|degradation/difference/differential MOS (DMOS)|Difference between MOS values of reference and distorted images.|lower|`[0, 100]`|[[ref1]](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=762345)  [[ref2]](https://videoclarity.com/PDF/WPUnderstandingJNDMOSPSNR.pdf)|

## 2. Dependency

```bash
conda create -n iqa python=3.7 -y && conda activate iqa
python -m pip install pyyaml opencv-python tqdm pandas

# for psnr/ssim
python -m pip install scikit-image==0.18.2

# for ms-ssim/lpips
# test under cuda 10.x
python -m pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html

# for lpips
python -m pip install lpips==0.1.3
```

For BRISQUE and NIQE, MATLAB >= R2017b is required; for PIQE, MATLAB >= R2018b is required.

If you want to use `main.py` to run MATLAB scripts, i.e., call MATLAB in Python, you should install MATLAB package in Conda environment. Check [here](https://www.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-engine-for-python.html). My solution:

```bash
# given linux
cd "matlabroot/extern/engines/python"  # e.g., ~/Matlab/R2019b/extern/engines/python
conda activate iqa && python setup.py install
```

## 3. Evaluation

1. Edit `opt.yml`.
2. Run: `conda activate iqa && [CUDA_VISIBLE_DEVICES=0] python main.py -case div2k_qf10 [-opt opt.yml -clean]`. `[<args>]` are optional.
3. Output: CSV log files at `./logs/`.

Note:

- `tar`: target, e.g., enhanced compressed images.
- `dst`: distorted, e.g., jpeg-compressed images.
- `src`: source, e.g., raw/pristine images.
- The list of the evaluated images is based on `tar_dir`.

## 4. License

We adopt Apache License v2.0. For other licenses, please refer to the references.

If you find this repository helpful, you may cite:

```tex
@misc{2021xing3,
  author = {Qunliang Xing},
  title = {Image Quality Assessment Toolbox},
  howpublished = "\url{https://github.com/ryanxingql/image-quality-assessment-toolbox}",
  year = {2021},
  note = "[Online; accessed 11-April-2021]"
}
```
