import os
import glob
import shutil
import numpy as np
from fid import fid_score

tag = 'v1'
ref_dir = '/dir/to/reference/png/'
src_dir = '/dir/to/source/png/'
dst_dir = '/dir/to/distorted/png/'
csv_file_name = f'iqa-fid-{tag}.csv'

dst_path_lst = sorted(glob.glob(os.path.join(dst_dir, '*.png')))
num = len(dst_path_lst)

log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_dir):
    os.mkdir('logs')
csv_path = os.path.join(log_dir, csv_file_name)
fp = open(csv_path, 'w')

for str_ in [ref_dir, src_dir, dst_dir, csv_path]:
    print(str_)
    fp.write(str_ + '\n')

tmp_ref_dir = os.path.join(os.getcwd(), f'tmp-fid-ref-{tag}-dont-del')
tmp_src_dir = os.path.join(os.getcwd(), f'tmp-fid-src-{tag}-dont-del')
tmp_dst_dir = os.path.join(os.getcwd(), f'tmp-fid-dst-{tag}-dont-del')
if not os.path.exists(tmp_ref_dir):
    os.makedirs(tmp_ref_dir)
if not os.path.exists(tmp_src_dir):
    os.makedirs(tmp_src_dir)
if not os.path.exists(tmp_dst_dir):
    os.makedirs(tmp_dst_dir)

tmp_ref = os.path.join(tmp_ref_dir, 'ref-tmp.png')
tmp_src = os.path.join(tmp_src_dir, 'src-tmp.png')
tmp_dst = os.path.join(tmp_dst_dir, 'dst-tmp.png')

fp.write('im_name,src,dst,del\n')

im_name_lst = []
src_lst = []
dst_lst= []
del_lst = []
result_lst = []
for idx, dst_im in enumerate(dst_path_lst):
    im_name = dst_im.split('/')[-1].split('.')[0]
    im_name_lst.append(im_name)
    ref_im = os.path.join(ref_dir, im_name + '.png')
    src_im = os.path.join(src_dir, im_name + '.png')

    shutil.copy(ref_im, tmp_ref)
    shutil.copy(src_im, tmp_src)
    shutil.copy(dst_im, tmp_dst)

    src_lst.append(fid_score.main_func(tmp_ref_dir, tmp_src_dir))
    dst_lst.append(fid_score.main_func(tmp_ref_dir, tmp_dst_dir))
    del_lst.append(dst_lst[-1] - src_lst[-1])

    result = f'{im_name},{src_lst[-1]:.3f},{dst_lst[-1]:.3f},{del_lst[-1]:.3f}'
    print(f'{idx+1}/{num}: ' + result)
    result_lst.append(result)

result = f'ave.,{np.mean(src_lst):.3f},{np.mean(dst_lst):.3f},{np.mean(del_lst):.3f}'
print(result)
fp.write(result + '\n')

for idx in range(num):
    fp.write(result_lst[idx] + '\n') 
fp.close()

shutil.rmtree(tmp_ref_dir)
shutil.rmtree(tmp_src_dir)
shutil.rmtree(tmp_dst_dir)
