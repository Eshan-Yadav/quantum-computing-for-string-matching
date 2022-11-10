import matplotlib.pyplot as plt
import numpy as np
import math
  
# # Using Numpy to create an array X
# X = np.arange(0, math.pi*2, 0.05)
  
# # Assign variables to the y axis part of the curve
# y = np.sin(X)
# z = np.cos(X)
  
# # Plotting both the curves simultaneously
# plt.plot(X, y, color='r', label='sin')
# plt.plot(X, z, color='g', label='cos')
  
# # Naming the x-axis, y-axis and the whole graph
# plt.xlabel("Angle")
# plt.ylabel("Magnitude")
# plt.title("Sine and Cosine functions")
  
# # Adding legend, which helps us recognize the curve according to it's color
# plt.legend()
  
# # To load the display window
# plt.show()


# plotting a graph of x=x
x = np.arange(0, 100, 1)
y = x
plt.plot(x, y, color='r', label='x=x')
plt.xlabel("x")
plt.ylabel("y")

plt.legend()


# plotting a graph of x^0.5
# x = np.arange(0, 10, 0.1)
y = np.sqrt(x)
plt.plot(x, y, color='g', label='x^0.5')
plt.xlabel("Number Of Inputs")
plt.ylabel("Time Complexity")

plt.legend()
plt.show()