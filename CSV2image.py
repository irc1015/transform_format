import numpy as np
import matplotlib.pyplot as plt

MAX_EPOCHES = 100

x = np.arange(1, MAX_EPOCHES, 1)
y_value = []

ex_values = np.genfromtxt('/Users/zhuzhirui/Desktop/1/1.csv', delimiter=',')#transform into numpy

n1 = np.delete(ex_values, 0, 0)#remove 1st line (name line)
n2 = np.delete(n1, 0, 1)#remove 1st column (epoch number colomn)

values = n2[:MAX_EPOCHES]
'''
0:train/box_loss 
1:train/obj_loss 
2:train/cls_loss 
3:metrics/precision 
4:metrics/recall
5:metrics/mAP_0.5 
6:metrics/map_0.5:0.95 
7:val/box_loss 
8:val/obj_loss 
9:val/cls_loss
10:x/lr0 
11:x/lr1 
12:x/lr2
'''
precision = [i for i in values[:, 3]]
precision = np.stack(precision)

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(x, precision, 'o-', label='YOLOv5s')
ax.set(xlabel='epoches', ylabel='precision')
ax.legend(loc='lower right')
plt.show()




