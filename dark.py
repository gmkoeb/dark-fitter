import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import leastsq 
from sklearn.metrics import r2_score 

data = np.loadtxt('exampledata.txt') 
x = data[:, 0]/32 #the voltage was divided by 32 because we had 32 solar cells operating in series
y = data[:, 1]


def func1(params, x, y): 
    a, b, c = params[0], params[1], params[2]
    residual = y-(a*(np.exp(b*(x-y*c))-1))
    return residual

def func2(params, x, y):
    a, b, c = params[0], params[1], params[2]
    residual = y-(((x-a*(y**(0.5)))/b)+c*(np.exp(40*(x-a*(y**(0.5))))-1))
    return residual

def func3(params, x, y):
    a = params[0]
    residual = y-(a*x**2)
    return residual

params = [0.000005, 0.1, 100] 
result = leastsq(func1, params, (x, y)) 
a, b, c = result[0][0], result[0][1], result[0][2]
yfit1 = (a*(np.exp(b*(x-y*c))-1)) 

params = [5*10**(0), 500*10**(1) , 0.0000000000001]
result = leastsq(func2, params, (x, y)) 
a, b, c = result[0][0], result[0][1], result[0][2]
yfit= ((x-a*(y**(0.5)))/b)+c*(np.exp(40*(x-a*(y**(0.5))))-1)

params = [0.5] 
result = leastsq(func3, params, (x, y)) 
a = result[0][0]
yfit2 = (a*x**2) 

correlation_matrix = np.corrcoef(y, yfit)

correlation_xy = correlation_matrix[0,1]

r2 = correlation_xy**2

fig = plt.figure(figsize=(6, 6))


sub1 = fig.add_subplot(221) 
sub1.plot(x, y, 'bo', markevery=20, label="Experimental")
sub1.plot(x, yfit, 'r-', label="Fit")
sub1.legend(loc='best', fancybox=True, shadow=True)
sub1.set_xscale('log')
sub1.set_yscale('log')

sub1.set_xlabel('V(V)')
sub1.set_ylabel('J(A/m²)')

custom_xlim1 = (0.2, 1)
custom_ylim1 = (0.0002, 0.05)
plt.setp(sub1, xlim=custom_xlim1, ylim=custom_ylim1)

sub2 = fig.add_subplot(222) 
sub2.plot(x, y, 'bo', markevery=20, label="Experimental")
sub2.plot(x, yfit2, 'r-', label="Fit")
sub2.legend(loc='best', fancybox=True, shadow=True)
sub2.set_xscale('log')
sub2.set_yscale('log')

sub2.set_xlabel('V(V)')
sub2.set_ylabel('J(A/m²)')
custom_xlim2 = (0.2, 1)
custom_ylim2 = (0.0002, 0.05)
plt.setp(sub2, xlim=custom_xlim2, ylim=custom_ylim2)

sub3 = fig.add_subplot(223) 
sub3.plot(x, y, 'bo', markevery=20, label="Experimental")
sub3.plot(x, yfit1, 'r-', label="Fit")
sub3.legend(loc='best', fancybox=True, shadow=True)
sub3.set_yscale('log')
sub3.set_xlabel('V(V)')
sub3.set_ylabel('J(A/m²)')

plt.tight_layout()
plt.show()

plt.show()
