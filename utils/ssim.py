from skimage.metrics import structural_similarity


class SSIM:
    def __init__(self):
        self.win_size = None
        self.gradient = False
        self.data_range = 255
        self.multichannel = True
        self.gaussian_weights = False
        self.full = False

    def forward(self, img1, img2):
        """
        input:
            img1/img2: (H W C) uint8 ndarray.
        return:
            ssim score, float.

        ref:
            why is it different from the MATLAB version: https://github.com/scikit-image/scikit-image/issues/4985
        """
        img1, img2 = img1.copy(), img2.copy()
        return structural_similarity(img1, img2, win_size=self.win_size, gradient=self.gradient,
                                     data_range=self.data_range, multichannel=self.multichannel,
                                     gaussian_weights=self.gaussian_weights, full=self.full)
