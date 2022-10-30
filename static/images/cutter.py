from PIL import Image
import numpy as np
import matplotlib.pylab as plt
import os
import json


def cut(img):
    for i in range(len(img)):
        if len(np.unique(img[i])) != 1:
            return img[i-40:, :]
        
def croop_and_count(file_path):
    img = np.array(Image.open(file_path).convert('L'))
    img = (img>128)*255

    for i in range(2):
        img = cut(img)
        img = img.T
        img = cut(img)
        img = img.T

        img = img[::-1, :]
        img = img[:, ::-1]

    plt.imshow(img)

    imgt = img[500:, :].T
    plt.imshow(imgt)
    count = 0
    for i in range(1, len(imgt)):
        count += int(len(np.unique(imgt[i])) != len(np.unique(imgt[i-1]))) 

    img = Image.fromarray(img.astype('uint8'))
    img.save(file_path)

    return count


if __name__ == '__main__':
    files = os.listdir('images/')
    files.sort()
    l1 = [] 
    l2 = []
    l3 = []
    d = {}
    c = 0
    for file in files:
        question_img, col_answers, rigth_answ = file, croop_and_count('images/' + file), "right"
        print(c)
        if c < 24:
            d = {'question_img' : question_img }
            d ['col_answers'] = col_answers
            d ['rigth_answ'] = rigth_answ
            l1.append(d)
            c+=1
 
        if c >= 24 and c <50:
            d = {'question_img' : question_img }
            d ['col_answers'] = col_answers
            d ['rigth_answ'] = rigth_answ
            l2.append(d)
            c+=1

        if c > 49:
            d = {'question_img' : question_img }
            d ['col_answers'] = col_answers
            d ['rigth_answ'] = rigth_answ
            l3.append(d)
            c+=1
        # print(croop_and_count('images/' + file), file)
    print(l1, "\n","\n", l2, "\n", "\n", l3)

    with open ('questioons_base.json','w') as f:
        json.dump(l1,f, indent=2)
        json.dump(l2,f, indent=2)
        json.dump(l3,f, indent=2)




