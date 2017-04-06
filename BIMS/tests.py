#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试
"""
#%%
import matplotlib.pyplot as plt
import numpy as np
X = np.linspace(-5, 5, 100)
Y = X*X
plt.plot(X, Y, '--')
plt.show()

#%%
np.arange(0, 10, 1)
np.linspace(1, 10, 10)
np.logspace(1, 3, 20)

#%%
import numpy as np
def func(i):
    return i 
np.fromfunction(func, (10, ))

#%%
import numpy as np
np.arange(0, 60, 10).reshape(6,1) + np.arange(0, 6)
np.linspace(0, np.pi, 10)
np.pi
