function fit_niqe_model
    div2k_raw_dir = '/home/x/data/div2k/raw';
    img_struct = dir(fullfile(div2k_raw_dir, '*.png'));
    img_cell = {img_struct.name};
    img_cell_1 = {};
    for ii = 1:length(img_cell)
        fullpath = fullfile(div2k_raw_dir, img_cell(ii));
        fullpath = fullpath{1};
        img_cell_1{ii} = fullpath;
    end

    flickr2k_hr_dir = '/home/x/data/flickr2k/hr';
    img_struct = dir(fullfile(flickr2k_hr_dir, '*.png'));
    img_cell = {img_struct.name};
    img_cell_2 = {};
    for ii = 1:length(img_cell)
        fullpath = fullfile(flickr2k_hr_dir, img_cell(ii));
        fullpath = fullpath{1};
        img_cell_2{ii} = fullpath;
    end

    img_cell = [img_cell_1, img_cell_2];
    imds = imageDatastore(img_cell);
    niqe_model = fitniqe(imds);  % default block size is 96x96
    save('./niqe_model_div2k_raw_and_flickr2k_hr.mat', 'niqe_model');
end