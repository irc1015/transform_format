import os

end_img = os.listdir(os.path.join('/hy-tmp/dataset_yang', 'images'))
end_lab = os.listdir(os.path.join('/hy-tmp/dataset_yang', 'labels'))
print('images: ' + str(len(end_img)))
print('labels: ' + str(len(end_lab)))

lab_path = os.path.join('/hy-tmp/dataset_yang', 'labels')
for i in range(len(end_lab)):
    name = end_lab[i][:-4] + '.jpg'
    if name not in end_img:
        print(end_lab[i])
        os.remove(os.path.join(lab_path, end_lab[i]))

end_img = os.listdir(os.path.join('/hy-tmp/dataset_yang', 'images'))
end_lab = os.listdir(os.path.join('/hy-tmp/dataset_yang', 'labels'))
print('images: ' + str(len(end_img)))
print('labels: ' + str(len(end_lab)))
