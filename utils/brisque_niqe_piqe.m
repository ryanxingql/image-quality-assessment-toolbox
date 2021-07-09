% log_fp: str, log file path.
% tar_path_lst: cell, list of tar image paths.
% if_brisque/if_niqe/if_piqe/if_dst/if_src: logical
function brisque_niqe_piqe(log_fp, start_row, start_column, tar_path_lst, dst_dir, src_dir, if_brisque, if_niqe, if_piqe, if_dst, if_src, niqe_model_path)
    % read existing csv into cell A

    flog = fopen(log_fp, 'r');
    i = 1;
    tline = fgetl(flog);
    A{i} = tline;
    while ischar(tline)
        i = i + 1;
        tline = fgetl(flog);
        A{i} = tline;
    end
    fclose(flog);

    % re-write options

    flog = fopen(log_fp, 'w');
    for i = 1:(start_row - 1)
        fprintf(flog, '%s\n', A{i});
    end

    if start_column == 1
        header_row = 'img_name';  % char
    else
        header_row = A{start_row};
    end
    header_print_start = length(header_row) + 1;  % img_name will be added later

    % iqa

    nimg = size(tar_path_lst, 2);

    for idx_img = 1:nimg
        tar_img_path = tar_path_lst{idx_img};
        [~, img_stem, ext] = fileparts(tar_img_path);
        img_name = append(img_stem, ext);

        tar_img = imread(tar_img_path);
        if if_dst
            dst_img_path = fullfile(dst_dir, img_name);
            dst_img = imread(dst_img_path);
        end
        if if_src
            src_img_path = fullfile(src_dir, img_name);
            src_img = imread(src_img_path);
        end

        img_name = {img_stem};
        T = table(img_name);  % init for every image

        if start_column == 1
            record_row = img_stem;
        else
            record_row = A{start_row + idx_img};
        end
        record_print_start = length(record_row) + 1;  % img stem will be added later

        if if_brisque
            if idx_img == 1
                header_row = [header_row ',brisque_tar'];
            end
            brisque_tar = brisque(tar_img);
            T = [T table(brisque_tar)];  % add new column
            record_row = [record_row sprintf(',%.3f', brisque_tar)];
            if if_dst
                if idx_img == 1
                    header_row = [header_row ',brisque_dst'];
                end
                brisque_dst = brisque(dst_img);
                T = [T table(brisque_dst)];
                record_row = [record_row sprintf(',%.3f', brisque_dst)];
            end
            if if_src
                if idx_img == 1
                    header_row = [header_row ',brisque_src'];
                end
                brisque_src = brisque(src_img);
                T = [T table(brisque_src)];
                record_row = [record_row sprintf(',%.3f', brisque_src)];
            end
        end

        if if_niqe
            % load pretrained model if exist
            if niqe_model_path ~= -1
                load(niqe_model_path, 'niqe_model');
            else
                niqe_model = niqeModel;  % load default model
            end

            if idx_img == 1
                header_row = [header_row ',niqe_tar'];
            end
            niqe_tar = niqe(tar_img, niqe_model);
            T = [T table(niqe_tar)];
            record_row = [record_row sprintf(',%.3f', niqe_tar)];
            if if_dst
                if idx_img == 1
                    header_row = [header_row ',niqe_dst'];
                end
                niqe_dst = niqe(dst_img, niqe_model);
                T = [T table(niqe_dst)];
                record_row = [record_row sprintf(',%.3f', niqe_dst)];
            end
            if if_src
                if idx_img == 1
                    header_row = [header_row ',niqe_src'];
                end
                niqe_src = niqe(src_img, niqe_model);
                T = [T table(niqe_src)];
                record_row = [record_row sprintf(',%.3f', niqe_src)];
            end
        end

        if if_piqe
            if idx_img == 1
                header_row = [header_row ',piqe_tar'];
            end
            piqe_tar = piqe(tar_img);
            T = [T table(piqe_tar)];
            record_row = [record_row sprintf(',%.3f', piqe_tar)];
            if if_dst
                if idx_img == 1
                    header_row = [header_row ',piqe_dst'];
                end
                piqe_dst = piqe(dst_img);
                T = [T table(piqe_dst)];
                record_row = [record_row sprintf(',%.3f', piqe_dst)];
            end
            if if_src
                if idx_img == 1
                    header_row = [header_row ',piqe_src'];
                end
                piqe_src = piqe(src_img);
                T = [T table(piqe_src)];
                record_row = [record_row sprintf(',%.3f', piqe_src)];
            end
        end

        % write row to CSV

        if idx_img == 1  % write header
            fprintf(flog, '%s\n', header_row);
        end
        fprintf(flog, '%s\n', record_row);
        disp(['img_name' header_row(header_print_start:end)]);
        disp([img_stem record_row(record_print_start:end)]);

        % init or concat

        if idx_img == 1
            T_total = T;
        else
            T_total = [T_total; T];  % add new row
        end
    end

    % cal ave and write to CSV

    if start_column == 1
        record_row = 'ave.';
    else
        record_row = A{end-1};
    end
    record_print_start = length(record_row) + 1;

    for i = 2:width(T_total)
        record_row = [record_row sprintf(',%.3f', mean(T_total{:, i}))];
    end
    disp(['ave.' header_row(header_print_start:end)]);
    disp(['ave.' record_row(record_print_start:end)]);
    fprintf(flog, '%s\n', record_row);

    % print all
    disp(' ')
    disp(['ave.' header_row(10:end)]);  % skip img_name
    disp(record_row);

end
