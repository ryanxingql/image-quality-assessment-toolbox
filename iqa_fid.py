from pathlib import Path

from cleanfid import fid


def main(tag, mode, tar_path_lst, src_dir, dst_dir, if_dst):
    src_dir = Path(src_dir).resolve()

    if if_dst:
        dst_dir = Path(dst_dir).resolve()

    num = len(tar_path_lst)

    current_dir = Path(__file__).resolve().parent
    log_dir = current_dir / 'logs'
    if not log_dir.exists():
        log_dir.mkdir()
    csv_path = log_dir / f'iqa_fid_{tag}.csv'
    fp = open(csv_path, mode)

    _lst = [src_dir, dst_dir, csv_path] if if_dst else [src_dir, csv_path]
    for _str in _lst:
        print(_str)
        fp.write(str(_str) + '\n')

    fp.write('dst,tar,del\n')

    src_path_lst = [src_dir / tar_path.name for tar_path in tar_path_lst]
    tar_score = fid.compute_fid(tar_path_lst, src_path_lst)

    if if_dst:
        dst_path_lst = [dst_dir / tar_path.name for tar_path in tar_path_lst]
        dst_score = fid.compute_fid(dst_path_lst, src_path_lst)
        del_score = tar_score - dst_score
        result = f'{dst_score:.3f},{tar_score:.3f},{del_score:.3f}'

    else:
        result = f'{tar_score:.3f}'

    print(result)
    fp.write(result)
    fp.close()
