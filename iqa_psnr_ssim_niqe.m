function iqa_psnr_ssim_niqe(tag, mode, tar_path_lst, src_dir, dst_dir, if_src, if_dst)
    csv_file_name = ['iqa_psnr_ssim_niqe_', tag, '.csv'];

    save_dir = fullfile(pwd, 'logs');
    mkdir(save_dir);
    csv_file_path = fullfile(save_dir, csv_file_name);

    fid = fopen(csv_file_path, mode);

    if if_dst
        lst_ = {src_dir, csv_file_path};
    else
        lst_ = {src_dir, dst_dir, csv_file_path};
    end
    for str_ = lst_
        fprintf(fid, [str_{:}, '\n']);
    end

    [~, nimg] = size(tar_path_lst);

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
        tar_path = tar_path_lst{iimg};

        [~, img_stem, ext] = fileparts(tar_path);
        img_name = append(img_stem, ext);

        src_path = fullfile(src_dir, img_name);
        src = imread(src_path);

        tar = imread(tar_path);

        psnr_tar = [psnr_tar; psnr(tar, src)];
        ssim_tar = [ssim_tar; ssim(tar, src)];
        niqe_tar = [niqe_tar; niqe(tar)];

        if if_src  % only valid for NIQE-M
            niqe_src = [niqe_src; niqe(src)];
        end

        if if_dst
            dst_path = fullfile(dst_dir, img_name);
            dst = imread(dst_path);

            psnr_dst = [psnr_dst; psnr(dst, src)];
            psnr_delta = [psnr_delta; psnr_tar - psnr_dst];

            ssim_dst = [ssim_dst; ssim(dst, src)];
            ssim_delta = [ssim_delta; ssim_tar - ssim_dst];

            niqe_dst = [niqe_dst; niqe(dst)];
            niqe_delta = [niqe_delta; niqe_tar - niqe_dst];
        end

        if if_src  % only valid for NIQE-M
            if if_dst
                if iimg == 1
                    header = 'im_name,psnr_dst,psnr_tar,psnr_del,ssim_dst,ssim_tar,ssim_del,niqe_src,niqe_dst,niqe_tar,niqe_del\n';  % only comma, no blank!
                    fprintf(fid, header);
                    fprintf(header);
                end

                result = [img_stem, ...
                    sprintf(',%.3f', psnr_dst(end)), sprintf(',%.3f', psnr_tar(end)), sprintf(',%.3f', psnr_delta(end)), ...
                    sprintf(',%.3f', ssim_dst(end)), sprintf(',%.3f', ssim_tar(end)), sprintf(',%.3f', ssim_delta(end)), ...
                    sprintf(',%.3f', niqe_src(end)), sprintf(',%.3f', niqe_dst(end)), sprintf(',%.3f', niqe_tar(end)), sprintf(',%.3f', niqe_delta(end))];

                if iimg == nimg
                    result_ave = ['ave.', ...
                        sprintf(',%.3f', mean(psnr_dst)), sprintf(',%.3f', mean(psnr_tar)), sprintf(',%.3f', mean(psnr_delta)), ...
                        sprintf(',%.3f', mean(ssim_dst)), sprintf(',%.3f', mean(ssim_tar)), sprintf(',%.3f', mean(ssim_delta)), ...
                        sprintf(',%.3f', mean(niqe_src)), sprintf(',%.3f', mean(niqe_dst)), sprintf(',%.3f', mean(niqe_tar)), sprintf(',%.3f', mean(niqe_delta))];
                end

            else
                if iimg == 1
                    header = 'im_name,psnr_tar,ssim_tar,niqe_src,niqe_tar\n';
                    fprintf(fid, header);
                    fprintf(header);
                end

                result = [img_stem, ...
                    sprintf(',%.3f', psnr_tar(end)), ...
                    sprintf(',%.3f', ssim_tar(end)), ...
                    sprintf(',%.3f', niqe_src(end)), sprintf(',%.3f', niqe_tar(end))];

                if iimg == nimg
                    result_ave = ['ave.', ...
                        sprintf(',%.3f', mean(psnr_tar)), ...
                        sprintf(',%.3f', mean(ssim_tar)), ...
                        sprintf(',%.3f', mean(niqe_src)), sprintf(',%.3f', mean(niqe_tar))];
                end
            end

        else
            if if_dst
                if iimg == 1
                    header = 'im_name,psnr_dst,psnr_tar,psnr_del,ssim_dst,ssim_tar,ssim_del,niqe_dst,niqe_tar,niqe_del\n';
                    fprintf(fid, header);
                    fprintf(header);
                end

                result = [img_stem, ...
                    sprintf(',%.3f', psnr_dst(end)), sprintf(',%.3f', psnr_tar(end)), sprintf(',%.3f', psnr_delta(end)), ...
                    sprintf(',%.3f', ssim_dst(end)), sprintf(',%.3f', ssim_tar(end)), sprintf(',%.3f', ssim_delta(end)), ...
                    sprintf(',%.3f', niqe_dst(end)), sprintf(',%.3f', niqe_tar(end)), sprintf(',%.3f', niqe_delta(end))];

                if iimg == nimg
                    result_ave = ['ave.', ...
                        sprintf(',%.3f', mean(psnr_dst)), sprintf(',%.3f', mean(psnr_tar)), sprintf(',%.3f', mean(psnr_delta)), ...
                        sprintf(',%.3f', mean(ssim_dst)), sprintf(',%.3f', mean(ssim_tar)), sprintf(',%.3f', mean(ssim_delta)), ...
                        sprintf(',%.3f', mean(niqe_dst)), sprintf(',%.3f', mean(niqe_tar)), sprintf(',%.3f', mean(niqe_delta))];
                end

            else
                if iimg == 1
                    header = 'im_name,psnr_tar,ssim_tar,niqe_tar\n';
                    fprintf(fid, header);
                    fprintf(header);
                end

                result = [img_stem, ...
                    sprintf(',%.3f', psnr_tar(end)), ...
                    sprintf(',%.3f', ssim_tar(end)), ...
                    sprintf(',%.3f', niqe_tar(end))];

                if iimg == nimg
                    result_ave = ['ave.', ...
                        sprintf(',%.3f', mean(psnr_tar)), ...
                        sprintf(',%.3f', mean(ssim_tar)), ...
                        sprintf(',%.3f', mean(niqe_tar))];
                end
            end
        end

        result = [result, '\n'];
        fprintf(result);
        fprintf(fid, result);
    end

    fprintf(fid, result_ave);
    fclose(fid);
    fprintf([result_ave, '\n']);
end
