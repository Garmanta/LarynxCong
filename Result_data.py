import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as st

folder = str('sub_')

Sqerror = np.zeros([20,3,4])
TiMI =    np.zeros([20,4,4])
TrioMI =  np.zeros([20,3,4])
PreMI =   np.zeros([20,3,4])

for i in range(20): 
    Sqerror[i,:,:] =  np.load(folder + str(i+1) + '/Results/Sqerror.npy')
    TiMI[i,:,:]    =  np.load(folder + str(i+1) + '/Results/TiMI.npy')
    TrioMI[i,:,:]  =  np.load(folder + str(i+1) + '/Results/TrioMI.npy')
    PreMI[i,:,:]   =  np.load(folder + str(i+1) + '/Results/PreMI.npy')
    



#-------------------------------------------------------------------------------
#First image
#-------------------------------------------------------------------------------
PBsq = Sqerror[:,0,0] 
NBsq = Sqerror[:,1,0]
SBsq = Sqerror[:,2,0]
#st.t.interval(alpha=0.95, df=len(SBsq)-1, loc=np.mean(SBsq), scale=st.sem(SBsq)) 

boxplotdata = [PBsq, NBsq, SBsq]
fig , ax = plt.subplots()

ax.set_xticklabels(['Raw','No-blip', 'Synb0'])
ax.set_ylabel("Squared Error")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.grid(True)
ax.boxplot(boxplotdata, showfliers=False)


#ccddff
#-------------------------------------------------------------------------------
#Second image
#-------------------------------------------------------------------------------

PBsq = np.mean(Sqerror[:,0,:],axis=0)
NBsq = np.mean(Sqerror[:,1,:],axis=0)
SBsq = np.mean(Sqerror[:,2,:],axis=0)

fig2, ax2 = plt.subplots()

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.set_ylabel("Squared Error")
plt.grid(True)

ax2.plot(PBsq, color='#ffaa80', linestyle='--', marker='o', linewidth=0.7, label = 'Raw')
ax2.plot(NBsq, color='#ff5500', linestyle='--', marker='o', linewidth=0.7, label = 'No-blip')
ax2.plot(SBsq, color='#993300', linestyle='--', marker='o', linewidth=0.7, label = 'Synb0')
plt.legend()


plt.xticks(ticks = [0,1,2,3],labels =['Mean','b-0','b-1000','b-2000'])
plt.yticks(ticks = [0,0.025,0.05])
plt.show()


#-------------------------------------------------------------------------------
#Third image
#-------------------------------------------------------------------------------

BNmi = np.mean(TrioMI[:,0,:], axis = 0)
SBmi = np.mean(TrioMI[:,1,:], axis = 0)
SNmi = np.mean(TrioMI[:,2,:], axis = 0)
stdTrio = np.std(TrioMI, axis = 0)

x_index = np.array([1,2,3,4])
width = 0.25

fig3,ax3 =  plt.subplots()

ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_visible(False)
ax3.set_ylabel("Mutual Information")

ax3.bar(x_index - width, BNmi, width=width, color='#ffaa80', yerr = stdTrio[0,:], capsize= 3 ,label = 'Blip & No-blip')
ax3.bar(x_index        , SNmi, width=width, color='#ff5500',  yerr = stdTrio[1,:], capsize= 3 , label = 'Synb0 & No-blip')
ax3.bar(x_index + width, SBmi, width=width, color='#993300', yerr = stdTrio[2,:], capsize= 3,  label = 'Blip & Synb0')

plt.legend(loc = 4)
plt.xticks(ticks = [1,2,3,4], labels=['Mean','b-0','b-1000','b-2000'])
plt.yticks(ticks = [0,0.5,1,1.5])

#-------------------------------------------------------------------------------
#Fourth image
#-------------------------------------------------------------------------------

fig4,ax4 = plt.subplots()

ax4.plot(BNmi, color='#ffaa80', linestyle='--', marker='o', linewidth=0.7, label = 'Blip & No-blip')
ax4.plot(SNmi, color='#ff5500', linestyle='--', marker='o', linewidth=0.7, label = 'Synb0 & No-blip')
ax4.plot(SBmi, color='#993300', linestyle='--', marker='o', linewidth=0.7, label = 'Blip & Synb0')
plt.legend()
plt.grid(True)

ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.spines['bottom'].set_visible(False)
ax4.spines['left'].set_visible(False)
ax4.set_ylabel("Mutual Information")

plt.xticks(ticks = [0,1,2,3],labels =['Mean','b-0','b-1000','b-2000'])
plt.yticks(ticks = [1.3,1.4,1.5, 1.6])
