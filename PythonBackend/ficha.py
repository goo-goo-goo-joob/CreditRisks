import pandas as pd
import numpy as np
import io
import base64
import os
import gc
#import seaborn as sns

from tqdm import tqdm
import matplotlib.pyplot as plt

def predictPr(df, model):
    mas = []#np.ndarray(df.shape[0])
    # for i in range(df.shape[0]):
    #     mas.append(model.predict_proba(np.array(df.iloc[i]))[1])#[i] = model.predict_proba(np.array(df.iloc[i]))
    mas = model.predict_proba(df)[:,1]
    return mas

def impact(model, data, ficha, head, tail, n = 100, logx = False, legend = None, true_rate = None):

    if logx:
        # masX = np.logspace(np.log10(head), np.log10(tail),n)
        masX = np.linspace(head,tail,n)
    else:
        masX = np.linspace(head,tail,n)

    if data.ndim == 2:

        #много строк
        sm = []
        dfs = []
        last = []
        for i in range(data.shape[0]):
            last.append(data.iloc[i][ficha])
            df = pd.DataFrame([data.iloc[i]]*n)
            df[ficha] = masX
            sm.append(predictPr(df, model))
            dfs.append(df)

    else:
        # 1 строка
        last = data[ficha]
        dfs = pd.DataFrame([data]*n)
        dfs[ficha] = masX
        sm = predictPr(dfs, model)

    prnt(masX, sm, logx, legend, data.ndim, last, true_rate,ficha)

    return sm, dfs

def prnt(mas, sm, logx, legend, ndim, last, true_rate, ficha):
    plt.figure(figsize=(16, 8))
    sm = np.array(sm)

    if ndim == 1:
        color = plt.cm.tab10(1/float(5))
        if legend:
            plt.plot(mas,sm,label = legend[i],color=color)
        else:
            plt.plot(mas,sm,color=color)
        if true_rate:
            plt.scatter(last, true_rate, s=20, c=color)
    else:
        colors = [plt.cm.tab10(i/float(len(sm)-1)) for i in range(len(sm))]
        for i in range(len(sm)):
            if legend:
                plt.plot(mas,sm[i],label = legend[i], color=colors[i])
            else:
                plt.plot(mas,sm[i],  color=colors[i])
            if true_rate:
                plt.scatter(last, true_rate, s=20, c=colors[i])

    plt.xticks(fontsize=16)
    if logx:
        plt.xscale('log')
    plt.yticks(fontsize=16)
    plt.grid(True)
    plt.xlabel('parametr', fontsize=16)
    plt.ylabel('Defolt Rate', fontsize=16)
    plt.title(ficha, fontsize=20)
    plt.legend(loc="lower left", fontsize=16)
    #plt.show()

def plt_to_base64(x, ok, bad, size=5):
    """draw plot graph"""
    # border = borders(ok) if len(ok) > 0 else None
    iterator_ok = np.arange(len(x))[np.isin(x, ok)]
    iterator_bad = np.arange(len(x))[np.isin(x, bad)]
    plt.figure(figsize=(size, size))
    plt.grid(True)
    plt.title("Обработка выборки")
    plt.xlabel("#")
    plt.ylabel("Значение")
    # if border is not None:
    #     plt.hlines(border, 0, len(x) - 1, color="r", linestyles="dashed")
    # plt.scatter(iterator_ok, ok,   label="Хорошие значения")
    # plt.scatter(iterator_bad, bad, label="Промахи")
    plt.legend()
    b = io.BytesIO()
    plt.savefig(b, format="png")
    b.seek(0)
    return base64.b64encode(b.read()).decode()

def plt_graph_to_base64(model, data, head, tail,legend, ficha = 'year_-1_15004'):
    """draw plot graph"""
    # ficha = 'year_-1_15004'
    impact(model, data, ficha, head, tail,legend=legend)
    b = io.BytesIO()
    plt.savefig(b, format="png")
    b.seek(0)
    return base64.b64encode(b.read()).decode()