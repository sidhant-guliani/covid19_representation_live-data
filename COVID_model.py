


def mod_logistic(x,l,k,x_0):
    return l/(1+np.exp(-k*(x-x_0)))

def mod_gompertz(x,a,b,c):
    return(a*np.exp(-b*np.exp(-c*x))) 
