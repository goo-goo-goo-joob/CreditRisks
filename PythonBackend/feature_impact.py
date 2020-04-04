import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def impact(model, data, feature, head, tail, n=100, logx=False):
    masX = np.linspace(head, tail, n)
    df = pd.DataFrame(data)
    df = df.append([data] * (n - 1), ignore_index=True)
    for i in range(n):
        df.loc[i, feature] = masX[i]
    sm = model.predict_proba(df)
    prnt(masX, sm, logx, feature)

    return sm


def prnt(mas, sm, logx, feature):
    plt.figure(figsize=(12, 6))
    sm = np.array(sm)

    plt.plot(mas, sm)

    plt.xticks(fontsize=16)
    if logx:
        plt.xscale('log')
    plt.yticks(fontsize=16)
    plt.grid(True)
    plt.xlabel('Значение параметра', fontsize=16)
    plt.ylabel('Вероятность дефолта', fontsize=16)
    #plt.ylim([0, 1])
    #plt.title(feature, fontsize=20)


def plt_graph_to_base64(model, data, head, tail, feature):
    """draw plot graph"""
    impact(model, data, feature, head, tail)
    b = io.BytesIO()
    plt.savefig(b, format="png")
    b.seek(0)
    return b.read()
