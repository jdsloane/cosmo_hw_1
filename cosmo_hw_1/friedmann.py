import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy import optimize

H0 = 70/(3.08567758*10**19) #Hubble constant today in s^-1 (70 km/s/Mpc)
gyr = 3.15569*10**16 #Number of seconds in a Gyr
suffix = '.png'

def adot(a,om_rad,om_mat,om_de,w):
    """Calculates the time derivative of the scale factor when the scale
    factor is 'a'

    """
    return H0*np.sqrt( om_rad/a**2 + om_mat/a + om_de/a**(1+3*w) + (1 - om_rad - om_de - om_mat) )

def time(a,om_rad,om_mat,om_de,w):
    """Calculates the time a universe would have when the scale factor is
    'a'

    """
    return integrate.quad(lambda x: 1/adot(x,om_rad,om_mat,om_de,w),1,a)[0]

def scale(t,om_rad,om_mat,om_de,w): #Currently obsolete
    """Calculates the scale factor a universe would have when the time is
    't' (in seconds).

    """
    return optimize.minimize(lambda x: (time(x,om_rad,om_mat,om_de,w)-t)**2, 1, method='powell').x

def hubble(a,om_rad,om_mat,om_de,w):
    """Calculates the hubble 'constant' for a universe as a function of
    'a'.

    """
    return adot(a,om_rad,om_mat,om_de,w)/a

def density(a,om_rad,om_mat,om_de,w):
    """Calculates the various components of the density (in units of
    critical density at a=1 as a function of 'a'.

    """
    rho_rad = om_rad/a**4
    rho_mat = om_mat/a**3
    rho_de = om_de/a**(3+3*w)
    return np.array([rho_rad, rho_mat, rho_de, rho_rad+rho_mat+rho_de])

def t_start(om_rad,om_mat,om_de,w): #Currently obsolete
    """Returns the time (or *A* time) that the scale factor is equal to zero.
    
    """
    return time(0,om_rad,om_mat,om_de,w)

if __name__ == '__main__':
    
    om_rad = np.array([0, 0, 0, 0, 0, 0])
    om_mat = np.array([1, 2, 0.3, 0.3, 0.3, 0.3])
    om_de = np.array([0, 0, 0, 0.7, 0.7, 0.7])
    w = np.array([-1, -1, -1, -1, -2/3., -4/3.])
    uni = np.array(['EDS','Closed','Open','LCDM','Quint','Phant'])
    
    for i in range(len(uni)):
        
        #Note to future generations:
        # We need to change how the limits on 'As' are calculated based on which
        # universe we're in. The bulk beings are closing the tesseract!
        
        As = np.linspace(0,2,1000)
        times = np.array([time(a,om_rad[i],om_mat[i],om_de[i],w[i]) for a in As])
        hubbles = hubble(As,om_rad[i],om_mat[i],om_de[i],w[i])
        densitys = density(As,om_rad[i],om_mat[i],om_de[i],w[i])
        
        plt.plot(times/gyr,As,label=uni[i])
        plt.scatter(0,1,label='Today')
        plt.title('Scale Factor vs. Time')
        plt.xlabel('time [Gyr]')
        plt.ylabel('Scale Factor')
        plt.legend(loc='best')
        plt.savefig(uni[i]+'_scale'+suffix)
        plt.close()
    
        plt.semilogy(times/gyr,70*hubbles/H0,label=uni[i])
        plt.scatter(0,70,label='Today')
        plt.title('Hubble "Constant" vs. Time')
        plt.xlabel('time [Gyr]')
        plt.ylabel('log(H [km/s/Mpc])')
        plt.legend(loc='best')
        plt.savefig(uni[i]+'_hubble'+suffix)
        plt.close()
        
        if om_rad[i]>0:
            plt.semilogy(times/gyr,densitys[0,:],label=uni[i]+': Radiation')
        if om_mat[i]>0:
            plt.semilogy(times/gyr,densitys[1,:],label=uni[i]+': Matter')
        if om_de[i]>0:
            plt.semilogy(times/gyr,densitys[2,:],label=uni[i]+': Dark Energy')
        plt.semilogy(times/gyr,densitys[3,:],label=uni[i]+': Total')
        plt.scatter([0,0,0,0],[om_rad[i],om_mat[i],om_de[i],om_rad[i]+om_mat[i]+om_de[i]],label='Today')
        plt.title('Density vs. Time')
        plt.xlabel('time [Gyr]')
        plt.ylabel('log(density/critical_0)')
        plt.legend(loc='best')
        plt.savefig(uni[i]+'_density'+suffix)
        plt.close()
        