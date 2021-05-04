
$ReadOutTime=0.069

mkdir Noblip
mkdir Blip
mkdir Synbo
mkdir Synbo/INPUTS
mkdir Synbo/OUTPUTS
mkdir Preproc
mkdir Results


mrconvert dir-AP_dwi.nii -fslgrad dir-AP_dwi.bvec dir-AP_dwi.bval -json_import dir-AP_dwi.json dwi_raw.mif
mrconvert dir-PA_dwi.nii -fslgrad dir-PA_dwi.bvec dir-PA_dwi.bval -json_import dir-PA_dwi.json dwi_PA.mif
mrconvert T1w.nii.gz -json_import T1w.json Synbo/INPUTS/T1.nii.gz

dwidenoise dwi_raw.mif - | mrdegibbs - dwi_preproc.mif -axes 0,1
dwidenoise dwi_PA.mif - | mrdegibbs - dwi_PA_preproc.mif -axes 0,1
dwiextract dwi_preproc.mif - -bzero | mrmath - mean preproc_mean_b0.mif -axis 3
mrmath dwi_PA_preproc.mif mean -  -axis 3 | mrcat - preproc_mean_b0.mif  -axis 3 b0_appa.mif

echo "Noblip image --------------------------------------"
dwifslpreproc dwi_preproc.mif Noblip/noblip.mif -rpe_none -pe_dir ap -eddy_options " --slm=linear --repol"
echo "Blip image ----------------------------------------"
dwifslpreproc dwi_preproc.mif Blip/blip.mif -rpe_pair -se_epi b0_appa.mif -pe_dir ap -eddy_options " --slm=linear --repol"

mrconvert preproc_mean_b0.mif Synbo/INPUTS/b0.nii.gz
printf '%s\n' "0 1 0 0.069" "0 1 0  0" > Synbo/INPUTS/acqparams.txt

mrconvert OUTPUTS/b0_u.nii.gz b0_u.mif
mrconvert INPUTS/b0.nii.gz preproc_mean_b0.mif
mrcat preproc_mean_b0.mif b0_u.mif -axis 3 b0_appa_synbo.mif

cd Synbo
sudo docker run --rm \
--name Synbo \
-v $(pwd)/INPUTS/:/INPUTS/ \
-v $(pwd)/OUTPUTS:/OUTPUTS/ \
-v /usr/local/freesurfer/license.txt:/extra/freesurfer/license.txt \
--user $(id -u):$(id -g) \
hansencb/synb0:v1.1

cd ..

echo "Synbo image----------------------------------------"
dwifslpreproc dwi_preproc.mif Synbo/synbo.mif -rpe_pair -se_epi b0_appa_synbo.mif -pe_dir ap -eddy_options " --slm=linear --repol"

mv dwi_preproc.mif Preproc/dwi_preproc.mif

echo "Creating masks-------------------------------------"
dwi2mask Preproc/dwi_preproc.mif Preproc/preproc_mask.nii
dwi2mask Noblip/noblip.mif Noblip/noblip_mask.nii
dwi2mask Blip/blip.mif Blip/blip_mask.nii
dwi2mask Synbo/synbo.mif Synbo/synbo_mask.nii


echo "Extracting mean b values for preproc---------------"
mrconvert preproc_mean_b0.mif Preproc/preproc_mean_b0.nii
dwiextract Preproc/dwi_preproc.mif - -bzero | mrmath - mean Preproc/preproc_mean_b0.nii -axis 3
dwiextract Preproc/dwi_preproc.mif - -shells 1000 | mrmath - mean Preproc/preproc_mean_b1000.nii -axis 3
dwiextract Preproc/dwi_preproc.mif - -shells 2000 | mrmath - mean Preproc/preproc_mean_b2000.nii -axis 3
mrmath Preproc/dwi_preproc.mif mean Preproc/preproc_mean.nii -axis 3

echo "Extracting mean b values for Noblip-----------------"
dwiextract Noblip/noblip.mif - -bzero | mrmath - mean Noblip/noblip_mean_b0.nii -axis 3
dwiextract Noblip/noblip.mif - -shells 1000 | mrmath - mean Noblip/noblip_mean_b1000.nii -axis 3
dwiextract Noblip/noblip.mif - -shells 2000 | mrmath - mean Noblip/noblip_mean_b2000.nii -axis 3
mrmath Noblip/noblip.mif mean Noblip/noblip_mean.nii -axis 3

echo "Extracting mean b values for Blip-------------------"
dwiextract Blip/blip.mif - -bzero | mrmath - mean Blip/blip_mean_b0.nii -axis 3
dwiextract Blip/blip.mif - -shells 1000 | mrmath - mean Blip/blip_mean_b1000.nii -axis 3
dwiextract Blip/blip.mif - -shells 2000 | mrmath - mean Blip/blip_mean_b2000.nii -axis 3
mrmath Blip/blip.mif mean Blip/blip_mean.nii -axis 3

echo "Extracting mean b values for Synbo------------------"
dwiextract Synbo/synbo.mif - -bzero | mrmath - mean Synbo/synbo_mean_b0.nii -axis 3
dwiextract Synbo/synbo.mif - -shells 1000 | mrmath - mean Synbo/synbo_mean_b1000.nii -axis 3
dwiextract Synbo/synbo.mif - -shells 2000 | mrmath - mean Synbo/synbo_mean_b2000.nii -axis 3
mrmath Synbo/synbo.mif mean Synbo/synbo_mean.nii -axis 3

mrgrid Synbo/INPUTS/T1.nii.gz regrid -size 104,104,72 T1s.nii
echo "	Finish! "
python LarynxCong.py




















