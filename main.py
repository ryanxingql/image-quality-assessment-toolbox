import time
import argparse
from pathlib import Path

import yaml
import pandas as pd
import numpy as np
from cv2 import cv2


# Load options

parser = argparse.ArgumentParser()
parser.add_argument('--opt', '-opt', type=str, default='opt.yml', help='Path to option YAML file.')
parser.add_argument('--case', '-case', type=str, help='Specified case in YML.')
parser.add_argument('--log_dir', '-ld', type=str, default=None, help='Which directory to save log.')
parser.add_argument('--clean', '-clean', action='store_true', help='Clean all logs with the same case.')
args = parser.parse_args()

current_dir = Path(__file__).resolve().parent
opt_fp = current_dir / args.opt
with open(opt_fp, 'r') as fp:
    opts_dict = yaml.load(fp, Loader=yaml.FullLoader)
opts_dict = opts_dict[args.case]

args.tar_dir = opts_dict['tar_dir']
args.dst_dir = opts_dict['dst_dir']
args.src_dir = opts_dict['src_dir']

args.if_dst = opts_dict['if_dst']
args.if_src = opts_dict['if_src']

args.start_idx = opts_dict['start_idx']
args.max_num = opts_dict['max_num']

args.if_psnr = opts_dict['if_psnr']
args.if_ssim = opts_dict['if_ssim']
args.if_msssim = opts_dict['if_msssim']
args.if_lpips = opts_dict['if_lpips']
args.if_brisque = opts_dict['if_brisque']
args.if_niqe = opts_dict['if_niqe']
args.if_piqe = opts_dict['if_piqe']

args.niqe_model_path = str((current_dir / Path(opts_dict['niqe_model_path'])).resolve()) if opts_dict['niqe_model_path'] is not None else -1

# Modify path

if args.tar_dir.split('/')[0] == '~':
    args.tar_dir = Path.home() / ('/'.join(args.tar_dir.split('/')[1:]))
else:
    args.tar_dir = Path(args.tar_dir)

if args.if_dst:
    assert args.dst_dir is not None, 'NO DST DIR IS GIVEN!'
    if args.dst_dir.split('/')[0] == '~':
        args.dst_dir = Path.home() / ('/'.join(args.dst_dir.split('/')[1:]))
    else:
        args.dst_dir = Path(args.dst_dir)

if args.src_dir is not None:
    if args.src_dir.split('/')[0] == '~':
        args.src_dir = Path.home() / ('/'.join(args.src_dir.split('/')[1:]))
    else:
        args.src_dir = Path(args.src_dir)
else:
    assert not (args.if_src or args.if_psnr or args.if_ssim or args.if_msssim or args.if_lpips), 'NO SRC DIR IS GIVEN!'

# Make log dir

timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
log_name = f'log_{args.case}_{timestamp}.csv'
log_dir = current_dir / 'logs' if args.log_dir is None else Path(args.log_dir)
log_dir.mkdir(exist_ok=True)
log_fp = Path(log_dir / log_name)

if args.clean:
    old_log_lst = log_dir.glob(f'log_{args.case}_*.csv')
    for old_log in old_log_lst:
        old_log.unlink()

# Record options

opt_dict_ = dict(key_=['tar_dir', 'dst_dir', 'src_dir', 'if_dst', 'if_src', 'start_idx', 'max_num', 'niqe_model_path'],
                 value_=[args.tar_dir, args.dst_dir, args.src_dir, args.if_dst, args.if_src, args.start_idx,
                         args.max_num, args.niqe_model_path])
print('\nreview:')
print(log_fp)
for key_, value_ in zip(opt_dict_['key_'], opt_dict_['value_']):
    print(f'{key_}: {value_}')

df = pd.DataFrame(opt_dict_)
df.to_csv(log_fp, index=False, header=False)

# List images

if args.max_num == -1:
    tar_img_path_lst = sorted(Path(args.tar_dir).resolve().glob('*.png'))[args.start_idx:]
else:
    tar_img_path_lst = sorted(Path(args.tar_dir).resolve().glob('*.png'))[args.start_idx: args.start_idx + args.max_num]

num_img = len(tar_img_path_lst)
assert num_img != 0, 'NO IMAGES WERE FOUND!'
print(f'\n{num_img} images were found.')

# Python based

if args.if_psnr or args.if_ssim or args.if_msssim or args.if_lpips:
    print('\nPython based evaluators...')

    info_dict = dict(img_name=[])

    if args.if_psnr:
        from utils.psnr import PSNR

        psnr_func = PSNR().forward
        info_dict['psnr_tar'] = []
        if args.if_dst:
            info_dict['psnr_dst'] = []

    if args.if_ssim:
        from utils.ssim import SSIM

        ssim_func = SSIM().forward
        info_dict['ssim_tar'] = []
        if args.if_dst:
            info_dict['ssim_dst'] = []

    if args.if_msssim:
        from utils.msssim import MSSSIM

        msssim_func = MSSSIM().forward
        info_dict['msssim_tar'] = []
        if args.if_dst:
            info_dict['msssim_dst'] = []

    if args.if_lpips:
        from utils.lpips import LPIPS

        lpips_func = LPIPS().forward
        info_dict['lpips_tar'] = []
        if args.if_dst:
            info_dict['lpips_dst'] = []

    for idx_tar, tar_img_path in enumerate(tar_img_path_lst):
        img_stem = tar_img_path.stem
        img_name = tar_img_path.name
        src_img_path = args.src_dir / img_name
        if args.if_dst:
            dst_img_path = args.dst_dir / img_name

        tar_img = cv2.imread(str(tar_img_path))
        src_path = cv2.imread(str(src_img_path))  # for FR
        if args.if_dst:
            dst_img = cv2.imread(str(dst_img_path))

        info_dict['img_name'] = [img_stem]  # init for every image

        if args.if_psnr:
            info_dict['psnr_tar'] = [psnr_func(tar_img, src_path)]
            if args.if_dst:
                info_dict['psnr_dst'] = [psnr_func(dst_img, src_path)]

        if args.if_ssim:
            info_dict['ssim_tar'] = [ssim_func(tar_img, src_path)]
            if args.if_dst:
                info_dict['ssim_dst'] = [ssim_func(dst_img, src_path)]

        if args.if_msssim:
            info_dict['msssim_tar'] = [msssim_func(tar_img, src_path)]
            if args.if_dst:
                info_dict['msssim_dst'] = [msssim_func(dst_img, src_path)]

        if args.if_lpips:
            info_dict['lpips_tar'] = [lpips_func(tar_img, src_path)]
            if args.if_dst:
                info_dict['lpips_dst'] = [lpips_func(dst_img, src_path)]

        df = pd.DataFrame(info_dict)
        if idx_tar == 0:
            df_total = df  # for calculating ave.
        else:
            df_total = pd.concat([df_total, df])
        print(df.to_string(index=False, float_format='%.3f'))
        if idx_tar == 0:
            df.to_csv(log_fp, header=True, index=False, mode='a', float_format='%.3f')
        else:
            df.to_csv(log_fp, header=False, index=False, mode='a', float_format='%.3f')

    info_dict = dict(img_name=['ave.'])
    for key_, lst_ in df_total.iteritems():
        if key_ == 'img_name':
            continue
        info_dict[key_] = [np.mean(lst_)]
    df = pd.DataFrame(info_dict)
    print(df.to_string(index=False, float_format='%.3f'))
    df.to_csv(log_fp, header=False, index=False, mode='a', float_format='%.3f')

# MATLAB based

if args.if_brisque or args.if_niqe or args.if_piqe:
    print('\nMATLAB based evaluators...')
    import matlab.engine

    eng = matlab.engine.start_matlab()
    eng.addpath(str(current_dir / './utils'), nargout=0)

    start_row = len(opt_dict_['key_']) + 1
    start_column = args.if_psnr + args.if_ssim + args.if_msssim + args.if_lpips + 1
    if start_column > 1:
        start_column += 1
    tar_img_path_lst = [str(tar_img_path) for tar_img_path in tar_img_path_lst]
    eng.brisque_niqe_piqe(str(log_fp), start_row, start_column, tar_img_path_lst, str(args.dst_dir), str(args.src_dir),
                          args.if_brisque, args.if_niqe, args.if_piqe, args.if_dst, args.if_src, args.niqe_model_path, nargout=0)
    eng.quit()

print('\ndone.')
