import numpy as np
import time
import random as rnd
import json
import matplotlib.pyplot as plt
from PIL import Image
from scipy.stats import truncnorm

seedvalue = 7658
rnd.seed(seedvalue)
np.random.seed(seedvalue)

surface = np.zeros((50, 50))

surface[25, :] = 4
surface[26, :] = 4

surface[0, :] = 5
surface[:, 0] = 5
surface[49, :] = 5
surface[:, 49] = 5



idlist = list(range(50*50))
surfids = np.asarray(idlist).reshape((50, 50))

directions = [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1]]

directions_nocorner = [[-1, 0], [1, 0]]


#######Create random surface that should be reproduced. Change seed above to randomize this.


prob_spread = 0.15
prob_riv = 0.05

mind = []
for i in range(50*50):
    mind.append([0,0])

innlist = [0.2,0.5]

available_innovs = [0,1]

for i in range(6):
    if i > 0:
        for run in range(20):
            shufflelist = idlist
            np.random.shuffle(shufflelist)
            for agent in shufflelist:
                pos = np.argwhere(surfids == agent)[0]
                if len(available_innovs) > 0:
                    if i*20 + run == innlist[0]*100:
                        mind[agent][available_innovs[0]] = 1
                        available_innovs.remove(available_innovs[0])
                        innlist.remove(innlist[0])

                if sum(mind[agent]) > 0:
                    if rnd.random() < prob_spread:
                        if sum(mind[agent]) == 1:
                            ind = mind[agent].index(max(mind[agent]))
                            zerotiles = []
                            for dir in directions:
                                newdir = [pos[0]+ dir[0], pos[1]+ dir[1]]
                                try:
                                    if mind[surfids[newdir[0], newdir[1]]][ind] == 0 and surface[newdir[0], newdir[1]] == 0:
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
                                    if mind[surfids[newdir[0], newdir[1]]][0] == 0 and surface[newdir[0], newdir[1]] < 4:
                                        zerotiles.append(newdir)
                                    elif mind[surfids[newdir[0], newdir[1]]][1] == 0 and surface[newdir[0], newdir[1]] < 4:
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




    for e in idlist:
        ids = np.argwhere(surfids == e)[0].tolist()
        if mind[e] == [1,0]:
            surface[ids[0], ids[1]] = 1
        elif mind[e] == [0, 1]:
            surface[ids[0], ids[1]] = 2
        elif mind[e] == [1, 1]:
            surface[ids[0], ids[1]] = 3

    surface2 = surface.copy()
    surface2 = np.kron(surface2, np.ones((60, 60))).copy()
    for item in np.nditer(surface2, flags=['multi_index', 'refs_ok'], op_flags=['readwrite']):
        if item == 0:
            item[...] = 38
        elif item == 1:
            item[...] = 80
        elif item == 2:
            item[...] = 120
        elif item == 3:
            item[...] = 160
        elif item == 4:
            item[...] = 200
        elif item == 5:
            item[...] = 255

    surface2 = surface2.astype("int64")
    img = Image.fromarray(np.uint8(plt.cm.Reds(surface2)*255))
    if i == 0:
        dst = Image.new('RGB', (img.width * 6, img.height))
        dst.paste(img, (0, 0))
    else:
        dst.paste(img, (img.width * i, 0))

dst.show()

dst.save("example_demo.png")
np.save("repsurface", surface)


def mainfunc_uniform(params): #model with uniform priors
    inittime = int(time.time() * 1000000)

    while inittime > 2 ** 32:
        inittime = str(inittime)[1:]
        inittime = int(inittime)

    ###########initialization
    seedvalue = inittime

    rnd.seed(seedvalue)
    np.random.seed(seedvalue)

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

    prob_spread = params['spread']
    prob_riv = params['riv']

    mind = []
    for i in range(50 * 50):
        mind.append([0, 0])

    inntime = np.round(np.asarray([params['feat0'], params['feat1']]) * 100)

    available_innovs = [0, 1]

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

    with open('toymod_uniform.json',
              'a') as f:
        f.write(json.dumps({"Accuracy": aggregate, "Params": params, 'Seed': seedvalue}))
        f.write('\n')
    return aggregate

def mainfunc_normal(params): #model with Normal priors
    inittime = int(time.time() * 1000000)

    while inittime > 2 ** 32:
        inittime = str(inittime)[1:]
        inittime = int(inittime)

    ###########initialization
    seedvalue = inittime

    rnd.seed(seedvalue)
    np.random.seed(seedvalue)

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

    prob_spread = params['spread']
    prob_riv = params['riv']

    mind = []
    for i in range(50 * 50):
        mind.append([0, 0])

    inntime = np.round(np.asarray([params['feat0'], params['feat1']]) * 100)

    available_innovs = [0, 1]

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

    with open('toymod.json',
              'a') as f:
        f.write(json.dumps({"Accuracy": aggregate, "Params": params, 'Seed': seedvalue}))
        f.write('\n')
    return aggregate


def mainfunc_informative(params): #model with informative priors
    inittime = int(time.time() * 1000000)

    while inittime > 2 ** 32:
        inittime = str(inittime)[1:]
        inittime = int(inittime)

    ###########initialization
    seedvalue = inittime

    rnd.seed(seedvalue)
    np.random.seed(seedvalue)

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

    prob_spread = params['spread']
    prob_riv = params['riv']

    mind = []
    for i in range(50 * 50):
        mind.append([0, 0])

    inntime = np.round(np.asarray([params['feat0'], params['feat1']]) * 100)

    available_innovs = [0, 1]

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

    print(aggregate)

    with open('toymod_informative.json',
              'a') as f:
        f.write(json.dumps({"Accuracy": aggregate, "Params": params, 'Seed': seedvalue}))
        f.write('\n')
    return aggregate




num_iter = 100000

for iter in range(num_iter):
    surface_repsurface = np.load(
        "repsurface.npy")


    pbounds = {
        "spread": rnd.random(),
        "riv": rnd.random(),
        "feat0": rnd.random(),
        "feat1": rnd.random()
    }
    mainfunc_uniform(pbounds)

for iter in range(num_iter):
    surface_repsurface = np.load(
    "repsurface.npy")


    pbounds = {
        "spread": truncnorm.rvs((0 - 0.25) / 0.3, (1 - 0.25) / 0.3, loc=0.25, scale=0.3, size=1)[0],
        "riv": truncnorm.rvs((0 - 0.1) / 0.2, (1 - 0.1) / 0.2, loc=0.1, scale=0.2, size=1)[0],
        "feat0": truncnorm.rvs((0 - 0.25) / 0.3, (1 - 0.25) / 0.3, loc=0.25, scale=0.3, size=1)[0],
        "feat1": truncnorm.rvs((0 - 0.75) / 0.3, (1 - 0.75) / 0.3, loc=0.75, scale=0.3, size=1)[0]
    }
    mainfunc_normal(pbounds)

for iter in range(num_iter):
    surface_repsurface = np.load(
        "repsurface.npy")


    pbounds = {
        "spread": np.random.beta(5,20,size=1)[0],
        "riv": np.random.beta(2,20,size=1)[0],
        "feat0": np.random.beta(2, 5,size=1)[0],
        "feat1": np.random.beta(5, 2, size=1)[0]
    }
    mainfunc_informative(pbounds)




