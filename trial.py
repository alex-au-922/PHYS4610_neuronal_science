import numpy as np
import matplotlib.pyplot as plt

a = np.random.normal(loc= 0, scale = 3, size = 10000000)
start_val = -5
end_val = 5
density, x_val = np.histogram(a, bins = np.linspace(start_val, end_val, 100), density= True)
fig, ax = plt.subplots()
ax.plot(x_val[:-1], density)
plt.show()
