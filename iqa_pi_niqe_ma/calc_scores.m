function calc_scores(input_dir, GT_dir, cmp_dir, shave_width, verbose, csv_file_path)

addpath(genpath(fullfile(pwd, 'iqa_pi_niqe_ma')));  % add folders and their subfolders, compared to iqa_pi_niqe_ma.m

%% log file

fid = fopen(csv_file_path,'w');
if fid<0
    errordlg('File creation failed', 'Error');
end

for str_ = [GT_dir, cmp_dir, input_dir, csv_file_path]
    fprintf(fid, [str_, '\n']);
end
fprintf(fid, 'im_name,pi_ref,pi_src,pi_dst,pi_del,niqe_ref,niqe_src,niqe_dst,niqe_del,ma_ref,ma_src,ma_dst,ma_del\n');  % only comma, no blank!

%% Loading model

load modelparameters.mat
blocksizerow    = 96;
blocksizecol    = 96;
blockrowoverlap = 0;
blockcoloverlap = 0;

%% Reading file list

file_list = dir([input_dir,'/*.png']);
im_num = length(file_list);

%% Calculating scores

niqe_raw = [];
ma_raw = [];
pi_raw = [];
niqe_cmp = [];
ma_cmp = [];
pi_cmp = [];
niqe_enh = [];
ma_enh = [];
pi_enh = [];
niqe_delta = [];
ma_delta = [];
pi_delta = [];

for ii = 1:im_num
    
    if verbose
        fprintf(['\nCalculating scores for image ',num2str(ii),' / ',num2str(im_num)]);
    end
    
    % Reading and converting images

    im_name = file_list(ii).name;
    input_image_path = fullfile(input_dir, im_name);
    input_image = convert_shave_image(imread(input_image_path),shave_width);
    GD_image_path = fullfile(GT_dir, im_name);
    GD_image = convert_shave_image(imread(GD_image_path),shave_width);
    cmp_image_path = fullfile(cmp_dir, im_name);
    cmp_image = convert_shave_image(imread(cmp_image_path),shave_width);
    
    % Calculating scores

    niqe_raw = [niqe_raw; computequality(GD_image,blocksizerow,blocksizecol,...
        blockrowoverlap,blockcoloverlap,mu_prisparam,cov_prisparam)];
    ma_raw = [ma_raw; quality_predict(GD_image)];
    pi_raw = [pi_raw; (niqe_raw + (10 - ma_raw)) / 2];
    
    niqe_cmp = [niqe_cmp; computequality(cmp_image,blocksizerow,blocksizecol,...
        blockrowoverlap,blockcoloverlap,mu_prisparam,cov_prisparam)];
    ma_cmp = [ma_cmp; quality_predict(cmp_image)];
    pi_cmp = [pi_cmp; (niqe_cmp + (10 - ma_cmp)) / 2];
    
    niqe_enh = [niqe_enh; computequality(input_image,blocksizerow,blocksizecol,...
        blockrowoverlap,blockcoloverlap,mu_prisparam,cov_prisparam)];
    ma_enh = [ma_enh; quality_predict(input_image)];
    pi_enh = [pi_enh; (niqe_enh + (10 - ma_enh)) / 2];
    
    niqe_delta = [niqe_delta; niqe_enh - niqe_cmp];
    ma_delta = [ma_delta; ma_enh - ma_cmp];
    pi_delta = [pi_delta; pi_enh - pi_cmp];

    result = {
        sprintf('%s', im_name), ...
        sprintf('%.3f', pi_raw(end)), sprintf('%.3f', pi_cmp(end)), sprintf('%.3f', pi_enh(end)), sprintf('%.3f', pi_delta(end)), ...
        sprintf('%.3f', niqe_raw(end)), sprintf('%.3f', niqe_cmp(end)), sprintf('%.3f', niqe_enh(end)), sprintf('%.3f', niqe_delta(end)), ...
        sprintf('%.3f', ma_raw(end)), sprintf('%.3f', ma_cmp(end)), sprintf('%.3f', ma_enh(end)), sprintf('%.3f', ma_delta(end)), ...
        };
    result = [strjoin(result, ','), '\n'];
    fprintf(result);
    fprintf(fid, result);
end

result = {
    'ave.', ...
    sprintf('%.3f', mean(pi_raw)), sprintf('%.3f', mean(pi_cmp)), sprintf('%.3f', mean(pi_enh)), sprintf('%.3f', mean(pi_delta)), ...
    sprintf('%.3f', mean(niqe_raw)), sprintf('%.3f', mean(niqe_cmp)), sprintf('%.3f', mean(niqe_enh)), sprintf('%.3f', mean(niqe_delta)), ...
    sprintf('%.3f', mean(ma_raw)), sprintf('%.3f', mean(ma_cmp)), sprintf('%.3f', mean(ma_enh)), sprintf('%.3f', mean(ma_delta)), ...
    };
result = strjoin(result, ',');
fprintf([result, '\n']);
fprintf(fid, result);

end
