import shutil
from pathlib import Path

import numpy as np
from fid import fid_score

tag = 'arcnn_div2k_qf10'
src_dir = Path('/home/xql/data/div2k/raw').resolve()
dst_dir = Path('/home/xql/data/div2k/jpeg/qf10').resolve()
tar_dir = Path('/home/xql/data/pycharm/PowerQE/exp/arcnn_div2k_qf10/enhanced_images').resolve()
csv_file_name = f'iqa_fid_{tag}.csv'

tar_path_lst = sorted(tar_dir.glob('*.png'))
num = len(tar_path_lst)

current_dir = Path(__file__).resolve().parent
log_dir = current_dir / 'logs'
if not log_dir.exists():
    log_dir.mkdir()
csv_path = log_dir / f'iqa_fid_{tag}.csv'
fp = open(csv_path, 'w')

for str_ in [src_dir, dst_dir, tar_dir, csv_path]:
    print(str_)
    fp.write(str(str_) + '\n')

tmp_src_dir = current_dir / f'tmp_fid_src_{tag}_dont_del'
tmp_dst_dir = current_dir / f'tmp_fid_dst_{tag}_dont_del'
tmp_tar_dir = current_dir / f'tmp_fid_tar_{tag}_dont_del'
if not tmp_src_dir.exists():
    tmp_src_dir.mkdir()
if not tmp_dst_dir.exists():
    tmp_dst_dir.mkdir()
if not tmp_tar_dir.exists():
    tmp_tar_dir.mkdir()

tmp_src = tmp_src_dir / 'src_tmp.png'
tmp_dst = tmp_dst_dir / 'dst_tmp.png'
tmp_tar = tmp_tar_dir / 'tar_tmp.png'

fp.write('im_name,dst,tar,del\n')

im_name_lst = []
dst_lst = []
tar_lst = []
del_lst = []
result_lst = []
for idx, tar_im in enumerate(tar_path_lst):
    im_name = tar_im.stem
    im_name_lst.append(im_name)
    src_im = src_dir / (str(im_name) + '.png')
    dst_im = dst_dir / (str(im_name) + '.png')

    shutil.copy(src_im, tmp_src)
    shutil.copy(dst_im, tmp_dst)
    shutil.copy(tar_im, tmp_tar)

    dst_lst.append(fid_score.main_func(str(tmp_src_dir), str(tmp_dst_dir)))
    tar_lst.append(fid_score.main_func(str(tmp_src_dir), str(tmp_tar_dir)))
    del_lst.append(tar_lst[-1] - dst_lst[-1])

    result = f'{im_name},{dst_lst[-1]:.3f},{tar_lst[-1]:.3f},{del_lst[-1]:.3f}'
    print(f'{idx+1}/{num}: ' + result)
    result_lst.append(result)

result = f'ave.,{np.mean(dst_lst):.3f},{np.mean(tar_lst):.3f},{np.mean(del_lst):.3f}'
print(result)
fp.write(result + '\n')

for idx in range(num):
    fp.write(result_lst[idx] + '\n') 
fp.close()

shutil.rmtree(tmp_src_dir)
shutil.rmtree(tmp_dst_dir)
shutil.rmtree(tmp_tar_dir)
