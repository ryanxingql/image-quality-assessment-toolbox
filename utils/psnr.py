from skimage.metrics import peak_signal_noise_ratio


class PSNR:
    def __init__(self):
        self.data_range = 255

    def forward(self, img1, img2):
        """
        input:
            img1/img2: (H W C) uint8 ndarray.
        return:
            psnr score, float.
        """
        img1, img2 = img1.copy(), img2.copy()
        return peak_signal_noise_ratio(img1, img2, data_range=self.data_range)
