import lpips
import torch


class LPIPS:
    def __init__(self):
        """
        args:
            net: alex/vgg/squeeze
            if_spatial: return a score (False) or a map of scores (True).
        """
        self.net = 'alex'
        self.if_spatial = False

        self.lpips_fn = lpips.LPIPS(net=self.net, spatial=self.if_spatial, verbose=False)

        self.if_cuda = True if torch.cuda.is_available() else False
        if self.if_cuda:
            self.lpips_fn.cuda()

    def _preprocess(self, img):
        img = img[:, :, ::-1]  # (H W BGR) -> (H W RGB)
        img = img / (255. / 2.) - 1.  # -> [0, 2] -> [-1, 1]
        img = img.transpose(2, 0, 1)  # ([RGB] H W)
        out = torch.Tensor(img)
        out = torch.unsqueeze(out, 0)  # (1 [RGB] H W)
        if self.if_cuda:
            out = out.cuda()
        return out

    def forward(self, img1, img2):
        """
        input:
            img1/img2: (H W C) uint8 ndarray.
        return:
            lpips score, float.
        """
        img1, img2 = img1.copy(), img2.copy()
        img1, img2 = self._preprocess(img1), self._preprocess(img2)
        lpips_score = self.lpips_fn.forward(img1, img2)
        return lpips_score.item()
