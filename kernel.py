window_h = 0.2
def SeriesX(start,end,step=1):
    x = []
    for i in range((end-start)//step):
        x.append(start + i*step)
    x = np.array(x,dtype=float)
    return x

def GaussKernel(x,xi,h):
    u = (x-xi)/h
    return 1/np.sqrt(2*np.pi)*np.exp(-u**2/2)

def KernelEstimate(x,data):
    result = []
    for i in range(x.shape[0]):
        sum = 0
        for j in range(data.shape[0]):
            sum = sum + GaussKernel(x[i],data[j],window_h)
        result.append(sum)
    return result
