function calc_scores(tar_dir, src_dir, dst_dir, csv_file_path, if_src, if_dst)
    addpath(genpath(fullfile(pwd, 'iqa_pi_niqe_ma')));  % add folders and their subfolders, compared to iqa_pi_niqe_ma.m

    shave_width = 0;  % number of pixels to shave off image borders when calcualting scores
    verbose = false;  % set verbose option

    %% log file

    fid = fopen(csv_file_path,'w');
    if fid < 0
        errordlg('File creation failed', 'Error');
    end

    if if_src
        if if_dst
            for str_ = {src_dir, dst_dir, tar_dir, csv_file_path}
                fprintf(fid, [str_{1}, '\n']);
            end
        else
            for str_ = {src_dir, tar_dir, csv_file_path}
                fprintf(fid, [str_{1}, '\n']);
            end
        end
    else
        if if_dst
            for str_ = {dst_dir, tar_dir, csv_file_path}
                fprintf(fid, [str_{1}, '\n']);
            end
        else
            for str_ = {tar_dir, csv_file_path}
                fprintf(fid, [str_{1}, '\n']);
            end
        end
    end

    %% Loading model

    load modelparameters.mat
    blocksizerow    = 96;
    blocksizecol    = 96;
    blockrowoverlap = 0;
    blockcoloverlap = 0;

    %% Reading file list

    file_list = dir([tar_dir,'/*.png']);
    im_num = length(file_list);

    %% Calculating scores

    if if_src
        niqe_raw = [];
        ma_raw = [];
        pi_raw = [];
    end

    niqe_enh = [];
    ma_enh = [];
    pi_enh = [];

    if if_dst
        niqe_cmp = [];
        ma_cmp = [];
        pi_cmp = [];

        niqe_delta = [];
        ma_delta = [];
        pi_delta = [];
    end

    for ii = 1:im_num

        if verbose
            fprintf(['\nCalculating scores for image ',num2str(ii),' / ',num2str(im_num)]);
        end

        % Reading and converting images

        im_name = file_list(ii).name;
        input_image_path = fullfile(tar_dir, im_name);
        input_image = convert_shave_image(imread(input_image_path),shave_width);

        if if_src
            GD_image_path = fullfile(src_dir, im_name);
            GD_image = convert_shave_image(imread(GD_image_path),shave_width);
        end

        if if_dst
            cmp_image_path = fullfile(dst_dir, im_name);
            cmp_image = convert_shave_image(imread(cmp_image_path),shave_width);
        end

        % Calculating scores

        niqe_enh = [niqe_enh; computequality(input_image,blocksizerow,blocksizecol,...
            blockrowoverlap,blockcoloverlap,mu_prisparam,cov_prisparam)];
        ma_enh = [ma_enh; quality_predict(input_image)];
        pi_enh = [pi_enh; (niqe_enh + (10 - ma_enh)) / 2];

        if if_src
            niqe_raw = [niqe_raw; computequality(GD_image,blocksizerow,blocksizecol,...
                blockrowoverlap,blockcoloverlap,mu_prisparam,cov_prisparam)];
            ma_raw = [ma_raw; quality_predict(GD_image)];
            pi_raw = [pi_raw; (niqe_raw + (10 - ma_raw)) / 2];
        end

        if if_dst
            niqe_cmp = [niqe_cmp; computequality(cmp_image,blocksizerow,blocksizecol,...
                blockrowoverlap,blockcoloverlap,mu_prisparam,cov_prisparam)];
            ma_cmp = [ma_cmp; quality_predict(cmp_image)];
            pi_cmp = [pi_cmp; (niqe_cmp + (10 - ma_cmp)) / 2];

            niqe_delta = [niqe_delta; niqe_enh - niqe_cmp];
            ma_delta = [ma_delta; ma_enh - ma_cmp];
            pi_delta = [pi_delta; pi_enh - pi_cmp];
        end

        img_stem = strsplit(im_name, '.');

        if if_src
            if if_dst
                if ii == 1
                    fprintf(fid, 'im_name,pi_src,pi_dst,pi_tar,pi_del,niqe_src,niqe_dst,niqe_tar,niqe_del,ma_src,ma_dst,ma_tar,ma_del\n');  % only comma, no blank!
                end

                result = {
                    sprintf('%s', img_stem{1}), ...
                    sprintf('%.3f', pi_raw(end)), sprintf('%.3f', pi_cmp(end)), sprintf('%.3f', pi_enh(end)), sprintf('%.3f', pi_delta(end)), ...
                    sprintf('%.3f', niqe_raw(end)), sprintf('%.3f', niqe_cmp(end)), sprintf('%.3f', niqe_enh(end)), sprintf('%.3f', niqe_delta(end)), ...
                    sprintf('%.3f', ma_raw(end)), sprintf('%.3f', ma_cmp(end)), sprintf('%.3f', ma_enh(end)), sprintf('%.3f', ma_delta(end)), ...
                };

                if ii == im_num
                    result_ave = {
                        'ave.', ...
                        sprintf('%.3f', mean(pi_raw)), sprintf('%.3f', mean(pi_cmp)), sprintf('%.3f', mean(pi_enh)), sprintf('%.3f', mean(pi_delta)), ...
                        sprintf('%.3f', mean(niqe_raw)), sprintf('%.3f', mean(niqe_cmp)), sprintf('%.3f', mean(niqe_enh)), sprintf('%.3f', mean(niqe_delta)), ...
                        sprintf('%.3f', mean(ma_raw)), sprintf('%.3f', mean(ma_cmp)), sprintf('%.3f', mean(ma_enh)), sprintf('%.3f', mean(ma_delta)), ...
                    };
                end

            else
                if ii == 1
                    fprintf(fid, 'im_name,pi_src,pi_tar,niqe_src,niqe_tar,ma_src,ma_tar\n');
                end

                result = {
                    sprintf('%s', img_stem{1}), ...
                    sprintf('%.3f', pi_raw(end)), sprintf('%.3f', pi_enh(end)), ...
                    sprintf('%.3f', niqe_raw(end)), sprintf('%.3f', niqe_enh(end)), ...
                    sprintf('%.3f', ma_raw(end)), sprintf('%.3f', ma_enh(end)), ...
                };

                if ii == im_num
                    result_ave = {
                        'ave.', ...
                        sprintf('%.3f', mean(pi_raw)), sprintf('%.3f', mean(pi_enh)), ...
                        sprintf('%.3f', mean(niqe_raw)), sprintf('%.3f', mean(niqe_enh)), ...
                        sprintf('%.3f', mean(ma_raw)), sprintf('%.3f', mean(ma_enh)), ...
                    };
                end
            end

        else
            if if_dst
                if ii == 1
                    fprintf(fid, 'im_name,pi_dst,pi_tar,pi_del,niqe_dst,niqe_tar,niqe_del,ma_dst,ma_tar,ma_del\n');
                end

                result = {
                    sprintf('%s', img_stem{1}), ...
                    sprintf('%.3f', pi_cmp(end)), sprintf('%.3f', pi_enh(end)), sprintf('%.3f', pi_delta(end)), ...
                    sprintf('%.3f', niqe_cmp(end)), sprintf('%.3f', niqe_enh(end)), sprintf('%.3f', niqe_delta(end)), ...
                    sprintf('%.3f', ma_cmp(end)), sprintf('%.3f', ma_enh(end)), sprintf('%.3f', ma_delta(end)), ...
                };

                if ii == im_num
                    result_ave = {
                        'ave.', ...
                        sprintf('%.3f', mean(pi_cmp)), sprintf('%.3f', mean(pi_enh)), sprintf('%.3f', mean(pi_delta)), ...
                        sprintf('%.3f', mean(niqe_cmp)), sprintf('%.3f', mean(niqe_enh)), sprintf('%.3f', mean(niqe_delta)), ...
                        sprintf('%.3f', mean(ma_cmp)), sprintf('%.3f', mean(ma_enh)), sprintf('%.3f', mean(ma_delta)), ...
                    };
                end

            else
                if ii == 1
                    fprintf(fid, 'im_name,pi_tar,niqe_tar,ma_tar\n');
                end

                result = {
                    sprintf('%s', img_stem{1}), ...
                    sprintf('%.3f', pi_enh(end)), ...
                    sprintf('%.3f', niqe_enh(end)), ...
                    sprintf('%.3f', ma_enh(end)), ...
                };

                if ii == im_num
                    result_ave = {
                        'ave.', ...
                        sprintf('%.3f', mean(pi_enh)), ...
                        sprintf('%.3f', mean(niqe_enh)), ...
                        sprintf('%.3f', mean(ma_enh)), ...
                    };
                end
            end
        end

        result = [strjoin(result, ','), '\n'];
        fprintf(result);
        fprintf(fid, result);
    end

    result = strjoin(result_ave, ',');
    fprintf(fid, result);
    fclose(fid);
    fprintf([result, '\n']);
end
