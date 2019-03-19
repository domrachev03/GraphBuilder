import matplotlib.pyplot as plt
import numpy as np

xMin = -30
yMin = -30
xMax = 30
yMAx = 30

xValueMin = -100.
iterationSize = 0.02
xValueMax = 100.

xTicks = np.arange(int(xValueMin), int(xValueMax), 5)
yTicks = np.arange(int(xValueMin), int(xValueMax), 5)

g = input('y = ')
k = ""

for i in range(len(g)):
    if i > 0 and g[i-1] == 'x' and g[i] == '(':
        k += '*'+'('
        continue
    if i > 0 and g[i-1] == ')' and g[i] == '(':
        k += '*'+'('
        continue
    if i > 0 and '1234567890)'.find(str(g[i-1])) > 0 and g[i] == 'x':
        k += "*"+"(x)"
        continue
    if g[i] == '^':
        k += '**'
        continue
    if g[i] == 'x':
        k += '(x)'
        continue
    k+=g[i]

print(k)

xArgs = np.arange(xValueMin, xValueMax, iterationSize)
yArgs = [(eval(k.replace('x', str(i)))) for i in xArgs]


# plt.figure(figsize = (10, 10))
fig, ax = plt.subplots(figsize = (5, 5))

# ax.spines['left'].set_position('center')
# ax.spines['bottom'].set_position('center')
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xticks([])
plt.yticks([])

ax.axis([xMin, xMax, yMin, xMax])


ax.axvline(linewidth = 1, color = 'k')
ax.axhline(linewidth = 1, color = 'k')
ax.plot(xArgs, yArgs, 'k-')
ax.plot(np.zeros(len(yTicks)), yTicks, 'k_')
ax.plot(xTicks, np.zeros(len(xTicks)), 'k|')

for i in yTicks:
    ax.text(0.25, i, i)
for i in xTicks:
    ax.text(i, 0.5, i)

ax.plot(xArgs, yArgs, 'k-')

plt.grid(True)
plt.show()