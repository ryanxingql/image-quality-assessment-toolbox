tag = 'arcnn_div2k_qf10'
src_dir = '/home/xql/data/div2k/raw'
dst_dir = '/home/xql/data/div2k/jpeg/qf10'
tar_dir = '/home/xql/data/pycharm/PowerQE/exp/arcnn_div2k_qf10/enhanced_images'
csv_file_name = ['iqa_psnr_ssim_niqe_', tag, '.csv']

save_dir = fullfile(pwd, 'logs');
mkdir(save_dir);
csv_file_path = fullfile(save_dir, csv_file_name);

fid = fopen(csv_file_path, 'w');

for str_ = {src_dir, dst_dir, tar_dir, csv_file_path}
    fprintf(fid, [str_{1}, '\n']);
end
fprintf(fid, 'im_name,psnr_dst,psnr_tar,psnr_del,ssim_dst,ssim_tar,ssim_del,niqe_src,niqe_dst,niqe_tar,niqe_del\n');  % only comma, no blank!

tar_set = {dir(fullfile(tar_dir, '*.png')).name};
[~, nimg] = size(tar_set);

psnr_dst = [];
psnr_tar = [];
psnr_delta = [];
ssim_dst = [];
ssim_tar = [];
ssim_delta = [];
niqe_src = [];
niqe_dst = [];
niqe_tar = [];
niqe_delta = [];

for iimg = 1:nimg
    img_name = tar_set(iimg);
    
    src_path = fullfile(src_dir, img_name);
    src = imread(src_path{1});
    dst_path = fullfile(dst_dir, img_name);
    dst = imread(dst_path{1});
    tar_path = fullfile(tar_dir, img_name);
    tar = imread(tar_path{1});

    psnr_dst = [psnr_dst; psnr(dst, src)];
    psnr_tar = [psnr_tar; psnr(tar, src)];
    psnr_delta = [psnr_delta; psnr_tar - psnr_dst];
    
    ssim_dst = [ssim_dst; ssim(dst, src)];
    ssim_tar = [ssim_tar; ssim(tar, src)];
    ssim_delta = [ssim_delta; ssim_tar - ssim_dst];
    
    niqe_src = [niqe_src; niqe(src)];
    niqe_dst = [niqe_dst; niqe(dst)];
    niqe_tar = [niqe_tar; niqe(tar)];
    niqe_delta = [niqe_delta; niqe_tar - niqe_dst];

    img_stem = strsplit(img_name{1}, '.');
    result = [
        img_stem(1), ...
        sprintf('%.3f', psnr_dst(end)), sprintf('%.3f', psnr_tar(end)), sprintf('%.3f', psnr_delta(end)), ...
        sprintf('%.3f', ssim_dst(end)), sprintf('%.3f', ssim_tar(end)), sprintf('%.3f', ssim_delta(end)), ...
        sprintf('%.3f', niqe_src(end)), sprintf('%.3f', niqe_dst(end)), sprintf('%.3f', niqe_tar(end)), sprintf('%.3f', niqe_delta(end)), ...
    ];
    result = [strjoin(result, ','), '\n'];
    fprintf(result);
    fprintf(fid, result);

end

result = [
    {'ave.'}, ...
    sprintf('%.3f', mean(psnr_dst)), sprintf('%.3f', mean(psnr_tar)), sprintf('%.3f', mean(psnr_delta)), ...
    sprintf('%.3f', mean(ssim_dst)), sprintf('%.3f', mean(ssim_tar)), sprintf('%.3f', mean(ssim_delta)), ...
    sprintf('%.3f', mean(niqe_src)), sprintf('%.3f', mean(niqe_dst)), sprintf('%.3f', mean(niqe_tar)), sprintf('%.3f', mean(niqe_delta)), ...
];
result = strjoin(result, ',');
fprintf([result, '\n']);
fprintf(fid, result);

fclose(fid);
