tag = 'v1'
ref_dir = '/dir/to/reference/png/'
src_dir = '/dir/to/source/png/'
dst_dir = '/dir/to/distorted/png/'
csv_file_name = ['iqa-psnr-ssim-niqe-', tag, '.csv']

save_dir = fullfile(pwd, 'logs');
mkdir(save_dir);
csv_file_path = fullfile(save_dir, csv_file_name);

fid = fopen(csv_file_path, 'w');

for str_ = [ref_dir, src_dir, dst_dir, csv_file_path]
    fprintf(fid, [str_, '\n']);
end
fprintf(fid, 'im_name,psnr_src,psnr_dst,psnr_del,ssim_src,ssim_dst,ssim_del,niqe_ref,niqe_src,niqe_dst,niqe_del\n');  % only comma, no blank!

dst_set = {dir(fullfile(dst_dir, '*.png')).name};
[~, nimg] = size(dst_set);

psnr_src = [];
psnr_dst = [];
psnr_delta = [];
ssim_src = [];
ssim_dst = [];
ssim_delta = [];
niqe_ref = [];
niqe_src = [];
niqe_dst = [];
niqe_delta = [];

for iimg = 1:nimg
    img_name = dst_set(iimg);
    
    ref_path = fullfile(ref_dir, img_name);
    ref = imread(ref_path{1});
    src_path = fullfile(src_dir, img_name);
    src = imread(src_path{1});
    dst_path = fullfile(dst_dir, img_name);
    dst = imread(dst_path{1});

    psnr_src = [psnr_src; psnr(src, ref)];
    psnr_dst = [psnr_dst; psnr(dst, ref)];
    psnr_delta = [psnr_delta; psnr_dst - psnr_src];
    
    ssim_src = [ssim_src; ssim(src, ref)];
    ssim_dst = [ssim_dst; ssim(dst, ref)];
    ssim_delta = [ssim_delta; ssim_dst - ssim_src];
    
    niqe_ref = [niqe_ref; niqe(ref)];
    niqe_src = [niqe_src; niqe(src)];
    niqe_dst = [niqe_dst; niqe(dst)];
    niqe_delta = [niqe_delta; niqe_dst - niqe_src];

    result = [
        img_name, ...
        sprintf('%.3f', psnr_src(end)), sprintf('%.3f', psnr_dst(end)), sprintf('%.3f', psnr_delta(end)), ...
        sprintf('%.3f', ssim_src(end)), sprintf('%.3f', ssim_dst(end)), sprintf('%.3f', ssim_delta(end)), ...
        sprintf('%.3f', niqe_ref(end)), sprintf('%.3f', niqe_src(end)), sprintf('%.3f', niqe_dst(end)), sprintf('%.3f', niqe_delta(end)), ...
        ];
    result = [strjoin(result, ','), '\n'];
    fprintf(result);
    fprintf(fid, result);

end

result = [
    {'ave.'}, ...
    sprintf('%.3f', mean(psnr_src)), sprintf('%.3f', mean(psnr_dst)), sprintf('%.3f', mean(psnr_delta)), ...
    sprintf('%.3f', mean(ssim_src)), sprintf('%.3f', mean(ssim_dst)), sprintf('%.3f', mean(ssim_delta)), ...
    sprintf('%.3f', mean(niqe_ref)), sprintf('%.3f', mean(niqe_src)), sprintf('%.3f', mean(niqe_dst)), sprintf('%.3f', mean(niqe_delta)), ...
    ];
result = strjoin(result, ',');
fprintf([result, '\n']);
fprintf(fid, result);

fclose(fid);
