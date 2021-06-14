function iqa_pi_niqe_ma(tag, src_dir, dst_dir, tar_dir, if_src, if_dst)
    addpath iqa_pi_niqe_ma;

    csv_file_name = ['iqa_pi_niqe_ma_', tag, '.csv'];

    save_dir = fullfile(pwd, 'logs');
    mkdir(save_dir);
    csv_file_path = fullfile(save_dir, csv_file_name);

    % Calculate scores and save
    calc_scores(tar_dir, src_dir, dst_dir, csv_file_path, if_src, if_dst);
end
