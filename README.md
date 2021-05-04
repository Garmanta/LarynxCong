# LarynxCong


We would like to thank OpenNeuro and the Project Larynx for making available the dataset. To download follow this link: https://openneuro.org/datasets/ds002634/versions/3.0.0

To run the pipeline, download the files in this repertoir. Use LarynxCong.sh, which needs the LarynxCong.py file, in the file where the subject data is located. Please remove the identifier information and leave the files with the following protocol:

sub_XX_dir-AP_dwi.nii --> dir-AP_dwi.nii

After running the pipeline across all the desired subjects, run the result_data.py to concatenate the data and to generate the plots.


The following software is required:

Mrtrix3.0 \
FSL \
Synb0-Disco \
Docker\
