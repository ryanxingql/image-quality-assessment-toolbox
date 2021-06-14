import os
import yaml
import argparse
import matlab.engine
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument(
    '--opt', '-opt', type=str, default='opt.yml',
    help='path to option YAML file.'
)
parser.add_argument(
    '--case', '-case', type=str, default='rbqe_div2k_qf30',
    help='specified case in YML.'
)
args = parser.parse_args()

current_dir = Path(__file__).resolve().parent
opt_fp = current_dir / args.opt
with open(opt_fp, 'r') as fp:
    opts_dict = yaml.load(fp, Loader=yaml.FullLoader)
opts_dict = opts_dict[args.case]

tag = args.case
src_dir = opts_dict['src_dir']
dst_dir = opts_dict['dst_dir']
tar_dir = opts_dict['tar_dir']
if_src = 1 if opts_dict['if_src'] else 0
if_dst = 1 if opts_dict['if_dst'] else 0

print('MAIN: INFO')
for _item in [tag, src_dir, dst_dir, tar_dir, if_src, if_dst]:
    print(_item)

if opts_dict['if_lpips']:
    print('\nMAIN: evaluating LPIPS...')
    os.system(f'python iqa_lpips.py -tag {tag} -src_dir {src_dir} -dst_dir {dst_dir} -tar_dir {tar_dir} -if_dst {if_dst:d}')

if opts_dict['if_fid']:
    print('\nMAIN: evaluating FID...')
    os.system(f'python iqa_fid.py -tag {tag} -src_dir {src_dir} -dst_dir {dst_dir} -tar_dir {tar_dir} -if_dst {if_dst:d}')

if opts_dict['if_psnr']:
    print('\nMAIN: evaluating PSNR, SSIM and NIQE-M...')
    eng = matlab.engine.start_matlab()
    eng.iqa_psnr_ssim_niqe(tag, src_dir, dst_dir, tar_dir, if_src, if_dst, nargout=0)
    eng.quit()

if opts_dict['if_pi']:
    print('\nMAIN: evaluating PI, NIQE and MA...')
    eng = matlab.engine.start_matlab()
    eng.iqa_pi_niqe_ma(tag, src_dir, dst_dir, tar_dir, if_src, if_dst, nargout=0)
    eng.quit()
