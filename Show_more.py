import matplotlib.pyplot as plt
from matplotlib.pyplot import rcParams
import numpy as np
import random
ax =[]
ay = []
bx = []
by = []
cx = []
cy = []
dx = []
dy = []
ex = []
ey = []
ox = []
oy = []


num = 0
plt.ion()

plt.rcParams['figure.figsize'] =(10,10)
plt.rcParams['font.sans-serif'] =['SiHei']
# plt.rcParams['axes.unicode_minutes'] = False
plt.rcParams['lines.linewidth'] = 0.5

while num <100:
    plt.clf()
    plt.suptitle('Burn in',fontsize = 20)

    #CH1
    g1 = np.random.random()
    ax.append(num)
    ay.append(g1)
    tmptile = plt.subplot(2,3,1)
    tmptile.set_title('CH1')
    tmptile.set_xlabel('x_axis',fontsize = 10)
    tmptile.set_ylabel('Y_axis',fontsize = 10)
    plt.plot(ax,ay,'g-')
    #CH2
    bx.append(num)
    by.append(g1)
    tmptile = plt.subplot(2,3,2)
    tmptile.set_title('CH2')
    tmptile.set_xlabel('x_axis',fontsize = 10)
    tmptile.set_ylabel('Y_axis',fontsize = 10)
    plt.plot(bx,by,'y-')

    #CH3
    cx.append(num)
    cy.append(g1)
    tmptile = plt.subplot(2,3,3)
    tmptile.set_title('CH3')
    tmptile.set_xlabel('x_axis',fontsize = 10)
    tmptile.set_ylabel('Y_axis',fontsize = 10)
    plt.plot(cx,cy,'r-')

    #CH4
    dx.append(num)
    dy.append(g1)
    tmptile = plt.subplot(2,3,4)
    tmptile.set_title('CH4')
    tmptile.set_xlabel('x_axis',fontsize = 10)
    tmptile.set_ylabel('Y_axis',fontsize = 10)
    plt.plot(dx,dy,'y-')

    #CH5
    ex.append(num)
    ey.append(g1)
    tmptile = plt.subplot(2,3,5)
    tmptile.set_title('CH5')
    tmptile.set_xlabel('x_axis',fontsize = 10)
    tmptile.set_ylabel('Y_axis',fontsize = 10)
    plt.plot(ex,ey,'p-')

    #CH6
    ox.append(num)
    oy.append(g1)
    tmptile = plt.subplot(2,3,6)
    tmptile.set_title('CH6')
    tmptile.set_xlabel('x_axis',fontsize = 10)
    tmptile.set_ylabel('Y_axis',fontsize = 10)
    plt.plot(ox,oy,'b-')

    plt.pause(0.4)
    num = num+1

plt.ioff()
#plt.show()



