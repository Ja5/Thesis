import numpy as np
import matplotlib.pyplot as plt

plt.style.use('presentation')

print(plt.style.available)


plt.figure()
plt.subplot(121)

plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')

line_up, = plt.plot([1, 2, 3], label='Line 2')
line_down, = plt.plot([3, 2, 1], label='Line 1')
plt.legend([line_up, line_down], ['Line Up', 'Line Down'])

with plt.style.context(('mythesis')):
    plt.subplot(122)

    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title('Histogram of IQ')

    line_up, = plt.plot([1, 2, 3], label='Line 2')
    line_down, = plt.plot([3, 2, 1], label='Line 1')
    plt.legend([line_up, line_down], ['Line Up', 'Line Down'])


plt.show()
