import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


def mutual_information(hgram):
     """ Mutual information for joint histogram
     """
     # Convert bins counts to probability values
     pxy = hgram / float(np.sum(hgram))
     px = np.sum(pxy, axis=1) # marginal for x over y
     py = np.sum(pxy, axis=0) # marginal for y over x
     px_py = px[:, None] * py[None, :] # Broadcast to multiply marginals
     # Now we can do the calculation using the pxy, px_py 2D arrays
     nzs = pxy > 0 # Only non-zero pxy values contribute to the sum
     return np.sum(pxy[nzs] * np.log(pxy[nzs] / px_py[nzs]))


#Loading data -----------------------------------------------------------------
#------------------------------------------------------------------------------
#Number of data --> [0] = Normal data ; [1] = b0 ; [2] = b1000 ; [3] = b2000
# [4] = mask
ndata = 5

Parser = nib.load(os.path.join('Preproc',"preproc_mean.nii"))
x,y,z = Parser.get_fdata().shape

Preproc = np.zeros([ndata,x,y,z])

Preproc[0,:,:,:]= Parser.get_fdata()
Parser = nib.load(os.path.join('Preproc',"preproc_mean_b0.nii"))
Preproc[1,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Preproc',"preproc_mean_b1000.nii"))
Preproc[2,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Preproc',"preproc_mean_b2000.nii"))
Preproc[3,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Preproc',"preproc_mask.nii"))
Preproc[4,:,:,:] = Parser.get_fdata()


Noblip = np.zeros([ndata,x,y,z])
Parser = nib.load(os.path.join('Noblip',"noblip_mean.nii"))
Noblip[0,:,:,:]= Parser.get_fdata()  
Parser = nib.load(os.path.join('Noblip',"noblip_mean_b0.nii"))
Noblip[1,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Noblip',"noblip_mean_b1000.nii"))
Noblip[2,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Noblip',"noblip_mean_b2000.nii"))
Noblip[3,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Noblip',"noblip_mask.nii"))
Noblip[4,:,:,:] = Parser.get_fdata()


Blip = np.zeros([ndata,x,y,z])
Parser = nib.load(os.path.join('Blip',"blip_mean.nii"))
Blip[0,:,:,:]= Parser.get_fdata()
Parser = nib.load(os.path.join('Blip',"blip_mean_b0.nii"))
Blip[1,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Blip',"blip_mean_b1000.nii"))
Blip[2,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Blip',"blip_mean_b2000.nii"))
Blip[3,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Blip',"blip_mask.nii"))
Blip[4,:,:,:] = Parser.get_fdata()

Synbo = np.zeros([ndata,x,y,z])
Parser = nib.load(os.path.join('Synbo',"synbo_mean.nii"))
Synbo[0,:,:,:]= Parser.get_fdata()
Parser = nib.load(os.path.join('Synbo',"synbo_mean_b0.nii"))
Synbo[1,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Synbo',"synbo_mean_b1000.nii"))
Synbo[2,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Synbo',"synbo_mean_b2000.nii"))
Synbo[3,:,:,:] = Parser.get_fdata()
Parser = nib.load(os.path.join('Synbo',"synbo_mask.nii"))
Synbo[4,:,:,:] = Parser.get_fdata()

T1 = nib.load(os.path.join("T1s.nii"))
T1 = T1.get_fdata()



#Mask and Normalization-----------------------------------------------------------------------
#Scale = 1 gives normalization to 1, = 255 gives normalization to uint8, =65536 gives normalization to uint16
#---------------------------------------------------------------------------------------------
Scale = 1
for i in range(ndata - 1):
    Preproc[i,:,:,:] = ((Preproc[i,:,:,:] + np.min(Preproc[i,:,:,:])) * (Scale / np.max(Preproc[i,:,:,:]))) * Preproc[4,:,:,:]
    Noblip[i,:,:,:]  = ((Noblip[i,:,:,:] + np.min(Noblip[i,:,:,:])) * (Scale / np.max(Noblip[i,:,:,:]))) * Noblip[4,:,:,:]
    Blip[i,:,:,:]    = ((Blip[i,:,:,:] + np.min(Blip[i,:,:,:])) * (Scale / np.max(Blip[i,:,:,:]))) * Blip[4,:,:,:]
    Synbo[i,:,:,:]   = ((Synbo[i,:,:,:] + np.min(Synbo[i,:,:,:])) * (Scale / np.max(Synbo[i,:,:,:]))) * Synbo[4,:,:,:]


#Obtaining n-------------------------------------------------------------------
#------------------------------------------------------------------------------
# 0 --> Preproc - Blip ; 1 --> Noblip - Blip ; 2 --> Blip - Synbo 
nmask = np.zeros([3])
nmask[0] = np.count_nonzero(Preproc[4,:,:,:] + Blip[4,:,:,:] == 1) +  np.count_nonzero(Preproc[4,:,:,:] + Blip[4,:,:,:] == 2)/2
nmask[1] = np.count_nonzero(Noblip[4,:,:,:] + Blip[4,:,:,:] == 1)  +  np.count_nonzero(Noblip[4,:,:,:] + Blip[4,:,:,:] == 2) /2
nmask[2] = np.count_nonzero(Synbo[4,:,:,:] + Blip[4,:,:,:] == 1)   +  np.count_nonzero(Synbo[4,:,:,:] + Blip[4,:,:,:] == 2)  /2


#Squared error for Diffusion --------------------------------------------------
#------------------------------------------------------------------------------

sqerror = np.zeros([3,4])

for i in range(ndata - 1):
    sqerror[0,i] = np.sum((Preproc[i,:,:,:] - Blip[i,:,:,:])**2) / nmask[0]
    sqerror[1,i] = np.sum((Noblip[i,:,:,:] - Blip[i,:,:,:])**2)  / nmask[1]
    sqerror[2,i] = np.sum((Synbo[i,:,:,:] - Blip[i,:,:,:])**2)   / nmask[2]

    
#Mutual Information -----------------------------------------------------------
#------------------------------------------------------------------------------



bins = 20

#Check axis
dPreproc = np.sum(Preproc,axis = 1 )
dBlip = np.sum(Blip,axis = 1 )
dNoblip = np.sum(Noblip,axis = 1 ) 
dSynbo = np.sum(Synbo, axis = 1 )
dT1 = np.sum(T1, axis = 1 )

T1MI    =  np.zeros([4,4])
T1MIsl   = np.zeros([x,y])
TrioMI   = np.zeros([3,4])
TrioMIsl = np.zeros([x,y])
PreMI  = np.zeros([3,4])
PreMIsl =np.zeros([x,y])

for i in range ( ndata - 1):
    T1MIsl,_,_ = np.histogram2d(  dT1[:,:].ravel()  , dPreproc[i,:,:].ravel(), bins)
    T1MI[0,i]  = mutual_information(T1MIsl)
    
    T1MIsl,_,_ = np.histogram2d(  dT1[:,:].ravel()  , dBlip[i,:,:].ravel(), bins)
    T1MI[1,i]  = mutual_information(T1MIsl)
    
    T1MIsl,_,_ = np.histogram2d(  dT1[:,:].ravel()  , dNoblip[i,:,:].ravel(), bins)
    T1MI[2,i]  = mutual_information(T1MIsl)
    
    T1MIsl,_,_ = np.histogram2d(  dT1[:,:].ravel()  , dSynbo[i,:,:].ravel(), bins)
    T1MI[3,i]  = mutual_information(T1MIsl)
    
    
    
    TrioMIsl,_,_ = np.histogram2d(   dBlip[i,:,:].ravel()  , dNoblip[i,:,:].ravel(), bins)
    TrioMI[0,i]  = mutual_information(TrioMIsl)
    
    TrioMIsl,_,_ = np.histogram2d(   dBlip[i,:,:].ravel()  , dSynbo[i,:,:].ravel(), bins)
    TrioMI[1,i]  = mutual_information(TrioMIsl)
    
    TrioMIsl,_,_ = np.histogram2d(   dSynbo[i,:,:].ravel()  , dNoblip[i,:,:].ravel(), bins)
    TrioMI[2,i]  = mutual_information(TrioMIsl)    



    PreMIsl,_,_ = np.histogram2d(     dPreproc[i,:,:].ravel()  , dNoblip[i,:,:].ravel(), bins)
    PreMI[0,i] = mutual_information(PreMIsl)
    
    PreMIsl,_,_ =   np.histogram2d( dPreproc[i,:,:].ravel()  , dBlip[i,:,:].ravel(), bins)
    PreMI[1,i] = mutual_information(PreMIsl)
    
    PreMIsl,_,_ =  np.histogram2d(    dPreproc[i,:,:].ravel()  , dSynbo[i,:,:].ravel(), bins)
    PreMI[2,i] = mutual_information(PreMIsl)


#Saving data ------------------------------------------------------------------
#------------------------------------------------------------------------------


np.save('Results/Sqerror.npy', sqerror)
np.save('Results/TiMI.npy', T1MI)
np.save('Results/TrioMI.npy', TrioMI)
np.save('Results/PreMI.npy', PreMI)
 

