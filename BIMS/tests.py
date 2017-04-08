#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试
"""
#%%
import matplotlib.pyplot as plt
import numpy as np
X = np.linspace(-5, 5, 100)
Y = X * X
plt.plot(X, Y, '--')
plt.show()

#%%
np.arange(0, 10, 2)
np.linspace(1, 10, 5)
# np.logspace(1, 3, 20)

#%%
import numpy as np


def func(i):
    return i


np.fromfunction(func, (10, ))

#%%
import numpy as np
np.arange(0, 60, 10).reshape(6, 1) + np.arange(0, 6)
np.linspace(0, np.pi, 10)
np.pi

#%%
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 1000)
y = np.sin(x)
z = np.cos(x)

plt.figure(figsize=(6, 3))
plt.plot(x, y, label="$sin(x)$", color="red", linewidth=2)
plt.plot(x, z, "b--", label="$cos(x^2)$")
plt.xlabel("Time(s)")
plt.ylabel("Volt")
plt.title("PyPlot First Example")
# plt.ylim(-1.2, 1.2)
plt.legend()
plt.show()


#%%
import numpy as np
b = np.arange(12).reshape(3,4)
b.sum(axis = 0)
b.sum(axis = 1)
b.max(axis = 1)
