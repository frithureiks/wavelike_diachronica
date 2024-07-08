import numpy as np
import random as rnd
import pandas as pd
import matplotlib.pyplot as plt


table = pd.read_csv('reproruns_normal.csv') # set this to the file that should be reproduced
first = 'yes'
for setting in range(len(table)):
    print(setting/len(table))
    params = dict(table.iloc[setting,:])

    rnd.seed(int(params['Seed']))
    np.random.seed(int(params['Seed']))

    surface = np.zeros((50, 50))

    surface[25, :] = 4
    surface[26, :] = 4

    surface[0, :] = 5
    surface[:, 0] = 5
    surface[49, :] = 5
    surface[:, 49] = 5

    idlist = list(range(50 * 50))
    surfids = np.asarray(idlist).reshape((50, 50))

    directions = [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1]]

    directions_nocorner = [[-1, 0], [1, 0]]

    #######preset

    prob_spread = params['Params.spread']
    prob_riv = params['Params.riv']

    mind = []
    for i in range(50 * 50):
        mind.append([0, 0])

    inntime = np.round(np.asarray([params['Params.feat0'], params['Params.feat1']]) * 100)

    available_innovs = [0, 1]
    past_innovs = []


    for run in range(100):

        shufflelist = idlist
        np.random.shuffle(shufflelist)
        for agent in shufflelist:
            pos = np.argwhere(surfids == agent)[0]
            if len(available_innovs) > 0:
                if inntime[0] == run and 0 in available_innovs:
                    mind[agent][0] = 1
                    available_innovs.remove(0)

                elif inntime[1] == run and 1 in available_innovs:
                    mind[agent][1] = 1
                    available_innovs.remove(1)

            if sum(mind[agent]) > 0:
                if rnd.random() < prob_spread:
                    if sum(mind[agent]) == 1:
                        ind = mind[agent].index(max(mind[agent]))
                        zerotiles = []
                        for dir in directions:
                            newdir = [pos[0] + dir[0], pos[1] + dir[1]]
                            try:
                                if mind[surfids[newdir[0], newdir[1]]][ind] == 0 and surface[
                                    newdir[0], newdir[1]] == 0:
                                    zerotiles.append(newdir)
                            except:
                                continue
                        if len(zerotiles) > 0:
                            select = zerotiles[np.random.choice(range(len(zerotiles)), 1)[0]]

                            mind[surfids[select[0], select[1]]][ind] = 1

                    if sum(mind[agent]) == 2:
                        zerotiles = []
                        for dir in directions:
                            newdir = [pos[0] + dir[0], pos[1] + dir[1]]
                            try:
                                if mind[surfids[newdir[0], newdir[1]]][0] == 0 and surface[
                                    newdir[0], newdir[1]] < 4:
                                    zerotiles.append(newdir)
                                elif mind[surfids[newdir[0], newdir[1]]][1] == 0 and surface[
                                    newdir[0], newdir[1]] < 4:
                                    zerotiles.append(newdir)
                            except:
                                continue
                        if len(zerotiles) > 0:
                            select = zerotiles[np.random.choice(range(len(zerotiles)), 1)[0]]

                            mind[surfids[select[0], select[1]]][mind[surfids[select[0], select[1]]].index(0)] = 1

                #####crossing

                if rnd.random() < prob_riv:
                    for dir in directions_nocorner:
                        try:
                            newdir = surface[pos[0] + dir[0], pos[1] + dir[1]]
                            if newdir == 4:
                                try:
                                    newdir2 = surfids[pos[0] + dir[0] * 3, pos[1] + dir[1] * 3]
                                    if sum(mind[newdir2]) < 2:
                                        if sum(mind[agent]) == 1:
                                            ind = mind[agent].index(max(mind[agent]))
                                        if sum(mind[agent]) == 2:
                                            if sum(mind[newdir2]) == 1:
                                                ind = mind[newdir2].index(min(mind[newdir2]))
                                            if sum(mind[newdir2]) == 1:
                                                ind = np.random.choice([0, 1], 1)[0]
                                        mind[newdir2][ind] = 1
                                except:
                                    continue
                        except:
                            continue

        if run in [0,19,39,59,79,99]:
            surface2 = np.asarray(surface.copy(), dtype='object')
            for e in idlist:
                ids = np.argwhere(surfids == e)[0].tolist()
                if mind[e] == [1, 0]:
                    surface2[ids[0], ids[1]] = 1
                elif mind[e] == [0, 1]:
                    surface2[ids[0], ids[1]] = 2
                elif mind[e] == [1, 1]:
                    surface2[ids[0], ids[1]] = 3


            for e in idlist:
                ids = np.argwhere(surfids == e)[0].tolist()
                if mind[e] == [1,0]:
                    surface2[ids[0], ids[1]] = np.asarray([1,0])
                elif mind[e] == [0, 1]:
                    surface2[ids[0], ids[1]] = np.asarray([0, 1])
                elif mind[e] == [1, 1]:
                    surface2[ids[0], ids[1]] = np.asarray([1, 1])
                elif mind[e] == [0, 0]:
                    surface2[ids[0], ids[1]] = np.asarray([0, 0])

            if first == 'yes':
                globals()['matrix_' + str(run)] = surface2
            else:
                globals()['matrix_'+str(run)] = globals()['matrix_'+str(run)] + surface2

            if run == 99:
                surface_repsurface = np.load(
                    "repsurface.npy")
                for e in idlist:
                    ids = np.argwhere(surfids == e)[0].tolist()
                    if mind[e] == [1, 0]:
                        surface[ids[0], ids[1]] = 1
                    elif mind[e] == [0, 1]:
                        surface[ids[0], ids[1]] = 2
                    elif mind[e] == [1, 1]:
                        surface[ids[0], ids[1]] = 3

                aggregate = 0
                for row in range(50):
                    for col in range(50):
                        repag = surface_repsurface[row, col]
                        if repag < 4:
                            ag = surface[row, col]
                            if 0 in [repag, ag] and 3 in [repag, ag]:
                                aggregate += 1
                            elif 0 in [repag, ag] or 3 in [repag, ag]:
                                if 1 in [repag, ag] or 2 in [repag, ag]:
                                    aggregate += 0.5
                            elif 1 in [repag, ag] and 2 in [repag, ag]:
                                aggregate += 1

    first = 'no'
np.save('matrix_0.npy', matrix_0)
np.save('matrix_1.npy',matrix_19)
np.save('matrix_2.npy', matrix_39)
np.save('matrix_3.npy', matrix_59)
np.save('matrix_4.npy', matrix_79)
np.save('matrix_5.npy', matrix_99)


#First innovation
fig, axes = plt.subplots(1, 6, figsize=(18, 3))  

for idx in range(6):
    surface = np.load("matrix_"+ str(idx)+".npy",
                allow_pickle=True)
    
    surface2 = np.zeros(surface.shape, dtype=int)

    for i in range(surface.shape[0]):
        for j in range(surface.shape[1]):
            surface2[i, j] = surface[i, j][0]


        surface2 = surface2.astype("int64")
        max_val = np.max(surface2)
        if max_val != 0:  
            surface2 = surface2 / max_val
        
    img = plt.cm.Reds(surface2) * 255  
    img = img.astype(np.uint8)  

    axes[idx].imshow(img)
    axes[idx].axis('off')  

plt.tight_layout()
plt.show()

#Second innovation
fig, axes = plt.subplots(1, 6, figsize=(18, 3))  

for idx in range(6):
    surface = np.load("matrix_"+ str(idx)+".npy",
                allow_pickle=True)
    
    surface2 = np.zeros(surface.shape, dtype=int)

    for i in range(surface.shape[0]):
        for j in range(surface.shape[1]):
            surface2[i, j] = surface[i, j][1]


        surface2 = surface2.astype("int64")
        max_val = np.max(surface2)
        if max_val != 0:  
            surface2 = surface2 / max_val
        
    img = plt.cm.Reds(surface2) * 255  
    img = img.astype(np.uint8)  

    axes[idx].imshow(img)
    axes[idx].axis('off')  

plt.tight_layout()
plt.show()