import argparse
from pathlib import Path

import torch
import lpips
import numpy as np
from cv2 import cv2


def main(tag, src_dir, dst_dir, tar_dir, if_dst):
    src_dir = Path(src_dir).resolve()
    tar_dir = Path(tar_dir).resolve()

    if if_dst:
        dst_dir = Path(dst_dir).resolve()

    tar_path_lst = sorted(tar_dir.glob('*.png'))
    num = len(tar_path_lst)

    current_dir = Path(__file__).resolve().parent
    log_dir = current_dir / 'logs'
    if not log_dir.exists():
        log_dir.mkdir()
    csv_path = log_dir / f'iqa_lpips_{tag}.csv'
    fp = open(csv_path, 'w')

    _lst = [src_dir, dst_dir, tar_dir, csv_path] if if_dst else [src_dir, tar_dir, csv_path]
    for _str in _lst:
        print(_str)
        fp.write(str(_str) + '\n')


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

        @staticmethod
        def _preprocess(inp, mode):
            out = None
            if mode == 'im':
                im = inp[:, :, ::-1]  # (H W BGR) -> (H W RGB)
                im = im / (255. / 2.) - 1.  # -> [0, 2] -> [-1, 1]
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
    tar_lst = []
    del_lst = []
    result_lst = []

    for idx, tar_path in enumerate(tar_path_lst):
        im_name = tar_path.stem
        im_name_lst.append(im_name)

        src_path = src_dir / (str(im_name) + '.png')
        src = cv2.imread(str(src_path))

        tar = cv2.imread(str(tar_path))
        tar_lst.append(lpips_forward(src, tar))

        if if_dst:
            dst_path = dst_dir / (str(im_name) + '.png')
            dst = cv2.imread(str(dst_path))
            dst_lst.append(lpips_forward(src, dst))
            del_lst.append(tar_lst[-1] - dst_lst[-1])

            if idx == 0:
                fp.write('im_name,dst,tar,del\n')
            result = f'{im_name},{dst_lst[-1]:.3f},{tar_lst[-1]:.3f},{del_lst[-1]:.3f}'

        else:
            if idx == 0:
                fp.write('im_name,tar\n')
            result = f'{im_name},{tar_lst[-1]:.3f}'

        result_lst.append(result)
        print(f'{idx+1}/{num}: ' + result)

    if if_dst:
        result = f'ave.,{np.mean(dst_lst):.3f},{np.mean(tar_lst):.3f},{np.mean(del_lst):.3f}'
    else:
        result = f'ave.,{np.mean(tar_lst):.3f}'

    print(result)
    fp.write(result + '\n')

    for idx in range(num):
        fp.write(result_lst[idx] + '\n')
    fp.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', '-tag', type=str)
    parser.add_argument('--src_dir', '-src_dir', type=str)
    parser.add_argument('--dst_dir', '-dst_dir', type=str)
    parser.add_argument('--tar_dir', '-tar_dir', type=str)
    parser.add_argument('--if_dst', '-if_dst', type=int, default=1)
    args = parser.parse_args()
    main(args.tag, args.src_dir, args.dst_dir, args.tar_dir, args.if_dst)
