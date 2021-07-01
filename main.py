import yaml
import argparse
import matlab.engine
from pathlib import Path
import iqa_lpips
import iqa_fid


def _str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('BOOLEAN VALUE EXPECTED.')


parser = argparse.ArgumentParser()
parser.add_argument('--opt', '-opt', type=str, default='opt.yml', help='path to option YAML file.')
parser.add_argument('--case', '-case', type=str, default='rbqe_div2k_qf30', help='specified case in YML.')
parser.add_argument('--mode', '-mode', type=str, default='a', help='add (a) or write (w).')
parser.add_argument('--if_src', '-if_src', type=_str2bool, default=False,
                    help='if evaluate src for NIQE-M, PI, NIQE, MA.')
parser.add_argument('--if_dst', '-if_dst', type=_str2bool, default=False, help='if evaluate dst for all matrices.')
parser.add_argument('--start_idx', '-start_idx', type=int, default=0, help='start from the idx-th image.')
parser.add_argument('--max_num', '-max_num', type=int, default=-1, help='total num of images.')
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
mode = args.mode
if_src = args.if_src
if_dst = args.if_dst
start_idx = args.start_idx
max_num = args.max_num

if src_dir.split('/')[0] == '~':
    src_dir = Path.home() / ('/'.join(src_dir.split('/')[1:]))
if dst_dir.split('/')[0] == '~':
    dst_dir = Path.home() / ('/'.join(dst_dir.split('/')[1:]))
if tar_dir.split('/')[0] == '~':
    tar_dir = Path.home() / ('/'.join(tar_dir.split('/')[1:]))

print('MAIN: INFO')
for _item in [tag, src_dir, dst_dir, tar_dir, mode, if_src, if_dst, start_idx, max_num]:
    print(_item)

if max_num == -1:
    tar_path_lst = sorted(Path(tar_dir).resolve().glob('*.png'))[start_idx:]
else:
    tar_path_lst = sorted(Path(tar_dir).resolve().glob('*.png'))[start_idx: start_idx + max_num]

assert len(tar_path_lst) != 0, 'NOT FOUND!'

if opts_dict['if_lpips']:
    print('\nMAIN: evaluating LPIPS...')
    iqa_lpips.main(tag, mode, tar_path_lst, src_dir, dst_dir, if_dst)

if opts_dict['if_fid']:
    print('\nMAIN: evaluating FID...')
    iqa_fid.main(tag, mode, tar_path_lst, src_dir, dst_dir, if_dst)

tar_path_lst = [str(path_) for path_ in tar_path_lst]

if opts_dict['if_psnr']:
    print('\nMAIN: evaluating PSNR, SSIM and NIQE-M...')
    eng = matlab.engine.start_matlab()
    eng.iqa_psnr_ssim_niqe(tag, mode, tar_path_lst, str(src_dir), str(dst_dir), if_src, if_dst, nargout=0)
    eng.quit()

if opts_dict['if_pi']:
    print('\nMAIN: evaluating PI, NIQE and MA...')
    eng = matlab.engine.start_matlab()
    eng.iqa_pi_niqe_ma(tag, mode, tar_path_lst, str(src_dir), str(dst_dir), if_src, if_dst, nargout=0)
    eng.quit()
