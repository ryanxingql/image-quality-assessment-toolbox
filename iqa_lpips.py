import os
import glob
import torch
from cv2 import cv2

import lpips
import numpy as np

tag = 'v1'
src_dir = '/dir/to/source/png/'
dst_dir = '/dir/to/distorted/png/'
tar_dir = '/dir/to/target/png/'
csv_file_name = f'iqa_lpips_{tag}.csv'

tar_path_lst = sorted(glob.glob(os.path.join(tar_dir, '*.png')))
num = len(tar_path_lst)

log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_dir):
    os.mkdir('logs')
csv_path = os.path.join(log_dir, csv_file_name)
fp = open(csv_path, 'w')

for str_ in [src_dir, dst_dir, tar_dir, csv_path]:
    print(str_)
    fp.write(str_ + '\n')

fp.write('im_name,dst,tar,del\n')

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

im_name_lst = []
dst_lst = []
tar_lst= []
del_lst = []
result_lst = []
for idx, tar_path in enumerate(tar_path_lst):
    im_name = tar_path.split('/')[-1]
    src_path = os.path.join(src_dir, im_name)
    dst_path = os.path.join(dst_dir, im_name)
    
    src = cv2.imread(src_path)
    dst = cv2.imread(dst_path)
    tar = cv2.imread(tar_path)

    im_name_lst.append(im_name)
    dst_lst.append(lpips_forward(src, dst))
    tar_lst.append(lpips_forward(src, tar))
    del_lst.append(tar_lst[-1] - dst_lst[-1])

    result = f'{im_name},{dst_lst[-1]:.3f},{tar_lst[-1]:.3f},{del_lst[-1]:.3f}'
    result_lst.append(result)

    print(f'{idx+1}/{num}: ' + result)

result = f'ave.,{np.mean(dst_lst):.3f},{np.mean(tar_lst):.3f},{np.mean(del_lst):.3f}'
print(result)
fp.write(result + '\n')

for idx in range(num):
    fp.write(result_lst[idx] + '\n')
fp.close()
