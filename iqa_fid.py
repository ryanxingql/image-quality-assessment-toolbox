import os
import glob
import shutil
import numpy as np
from fid import fid_score

tag = 'v1'
src_dir = '/dir/to/source/png/'
dst_dir = '/dir/to/distorted/png/'
tar_dir = '/dir/to/target/png/'
csv_file_name = f'iqa_fid_{tag}.csv'

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

tmp_src_dir = os.path.join(os.getcwd(), f'tmp_fid_src_{tag}_dont_del')
tmp_dst_dir = os.path.join(os.getcwd(), f'tmp_fid_dst_{tag}_dont_del')
tmp_tar_dir = os.path.join(os.getcwd(), f'tmp_fid_tar_{tag}_dont_del')
if not os.path.exists(tmp_src_dir):
    os.makedirs(tmp_src_dir)
if not os.path.exists(tmp_dst_dir):
    os.makedirs(tmp_dst_dir)
if not os.path.exists(tmp_tar_dir):
    os.makedirs(tmp_tar_dir)

tmp_src = os.path.join(tmp_src_dir, 'src_tmp.png')
tmp_dst = os.path.join(tmp_dst_dir, 'dst_tmp.png')
tmp_tar = os.path.join(tmp_tar_dir, 'tar_tmp.png')

fp.write('im_name,dst,tar,del\n')

im_name_lst = []
dst_lst = []
tar_lst= []
del_lst = []
result_lst = []
for idx, tar_im in enumerate(tar_path_lst):
    im_name = tar_im.split('/')[-1].split('.')[0]
    im_name_lst.append(im_name)
    src_im = os.path.join(src_dir, im_name + '.png')
    dst_im = os.path.join(dst_dir, im_name + '.png')

    shutil.copy(src_im, tmp_src)
    shutil.copy(dst_im, tmp_dst)
    shutil.copy(tar_im, tmp_tar)

    dst_lst.append(fid_score.main_func(tmp_src_dir, tmp_dst_dir))
    tar_lst.append(fid_score.main_func(tmp_src_dir, tmp_tar_dir))
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
