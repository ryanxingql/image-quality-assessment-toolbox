import os
import glob
import torch
from cv2 import cv2

import lpips
import numpy as np

ref_dir = '/home/x/data/GitZone/FR/data/FFHQ/1024x1024_10k/raw'
src_dir = '/home/x/data/GitZone/FR/data/FFHQ/1024x1024_10k/jpeg/qf30'
dst_dir = '/home/x/data/GitZone/FR/exp/FR_512_QF30_noBN_noHiIN/img_enhanced_val'
csv_file_name = 'iqa_lpips.csv'

dst_lst = sorted(glob.glob(os.path.join(dst_dir, '*.png')))

log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_dir):
    os.mkdir('logs')
fp = open(os.path.join(log_dir, csv_file_name), 'w')

fp.write('im_name,lpips_src,lpips_dst,lpips_del\n')

class LPIPS(torch.nn.Module):
    """Learned Perceptual Image Patch Similarity.
    Args:
        if_spatial: return a score or a map of scores.
        im: cv2 loaded images, or ([RGB] H W), [0, 1] CUDA tensor.
    """
    def __init__(self, net='alex', if_spatial=False, if_cuda=False):
        super().__init__()

        self.lpips_fn = lpips.LPIPS(net=net, spatial=if_spatial)
        if if_cuda:
            self.lpips_fn.cuda()

    def _preprocess(self, inp, mode):
        out = None
        if mode == 'im':
            im = inp[:, :, ::-1]  # (H W BGR) -> (H W RGB)
            im = im / (255. / 2.)  - 1.  # -> [0, 2] -> [-1, 1]
            im = im[..., np.newaxis]  # (H W RGB 1)
            im = im.transpose(3, 2, 0, 1)  # (B=1 C=RGB H W)
            out = torch.Tensor(im)
        elif mode == 'tensor':
            out = inp * 2. - 1.
        return out

    def forward(self, ref, im):
        mode = 'im' if ref.dtype == np.uint8 else 'tensor'
        ref = self._preprocess(ref, mode=mode)
        im = self._preprocess(im, mode=mode)
        lpips_score = self.lpips_fn.forward(ref, im)
        return lpips_score.item()

lpips_forward = LPIPS().forward

lpips_src = []
lpips_dst= []
lpips_del = []

for dst_path in dst_lst:
    im_name = dst_path.split('/')[-1]
    ref_path = os.path.join(ref_dir, im_name)
    src_path = os.path.join(src_dir, im_name)
    
    ref = cv2.imread(ref_path)
    src = cv2.imread(src_path)
    dst = cv2.imread(dst_path)

    lpips_src.append(lpips_forward(ref, src))
    lpips_dst.append(lpips_forward(ref, dst))
    lpips_del.append(lpips_dst[-1] - lpips_src[-1])

    result = f'{im_name},{lpips_src[-1]:.3f},{lpips_dst[-1]:.3f},{lpips_del[-1]:.3f}'
    print(result)
    fp.write(result + '\n')

result = f'ave.,{np.mean(lpips_src):.3f},{np.mean(lpips_dst):.3f},{np.mean(lpips_del):.3f}'
print(result)
fp.write(result)

fp.close()
