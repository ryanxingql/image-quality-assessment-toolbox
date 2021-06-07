tag = 'v1'
src_dir = '/dir/to/source/png/'
dst_dir = '/dir/to/distorted/png/'
tar_dir = '/dir/to/target/png/'
csv_file_name = ['iqa_pi_niqe_ma_', tag, '.csv']

save_dir = fullfile(pwd, 'logs');
mkdir(save_dir);
csv_file_path = fullfile(save_dir, csv_file_name);

addpath iqa_pi_niqe_ma;

% Number of pixels to shave off image borders when calcualting scores
shave_width = 0;

% Set verbose option
verbose = false;

% Calculate scores and save
calc_scores(tar_dir, src_dir, dst_dir, shave_width, verbose, csv_file_path);
