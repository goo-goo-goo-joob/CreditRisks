from typing import Iterable, Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
from tqdm import tqdm_notebook


def _empty_iterator(seq, *args, **kwargs):
    for el in seq:
        yield el


def float_to_str(f: float, precision=1) -> str:
    return str(np.round(f * 100, decimals=precision))


def calc_multi_profits(y_true: np.ndarray, y_score: np.ndarray,
                       percents: Iterable[float],
                       lgds: Iterable[float]) -> Tuple[Dict[Tuple[float, float], np.ndarray], np.ndarray, np.ndarray]:
    """
    Calculate profit for different percents and lgd's
    :param y_true: true labels
    :param y_score: probabilities
    :param percents: percents to handle
    :param lgds: lgd to handle
    :return: Pair: Dict with keys (percent, lgd) and values as profit; threshold
    """
    profits = {}
    for percent in percents:
        for lgd in lgds:
            profits[(percent, lgd)] = []
    negative_count = (y_true == 0).sum()
    y_score_index = np.argsort(y_score)
    y_score = y_score[y_score_index]
    y_true = y_true[y_score_index]

    curr_bad = np.cumsum(y_true)
    curr_ok = np.cumsum((~y_true.astype(bool)).astype(np.int32))
    fp = negative_count - curr_ok
    fpr = fp / negative_count
    for percent in percents:
        for lgd in lgds:
            profit = (percent * curr_ok - lgd * curr_bad) / (percent * negative_count)
            profits[(percent, lgd)] = profit
    return profits, np.sort(y_score), np.array(fpr)


def default_percent_space():
    return np.linspace(0.15, 0.25, num=3)


def default_lgd_space():
    return np.linspace(0.8, 0.9, num=1)


def default_threshold_space():
    return np.linspace(0, 1, num=200)


def plt_profit(y_true: np.ndarray, y_score: np.ndarray,
               ax=None,
               title=None,
               percent_credit=None,
               y_lim=None,
               x_lim=None,
               percent_space=None,
               lgd_space=None):
    """Draws metrics based on profit from credit to bank,
    taking the values of threshold and interest on credit.

    Parameters
    ----------
    y_true : array, shape = [n_samples]
        True binary labels
    y_score : array, shape = [n_samples]
        Target scores, probability estimates of the positive class
    title : str
        The title to print
    percent_credit : float > 0 and <= 1, optional
        If not None, adds a graph corresponding to this parameter
    y_lim : array, shape = [2]
        The limits of graph by y-axis
    x_lim : array, shape = [2]
        The limits of graph by x-axis
    percent_space : array, shape = [>=1]
        The values of interest on credit to plot on graph
    lgd_space: array
        lgd to calculate
    """
    if percent_space is None:
        percent_space = default_percent_space()
    if percent_credit is not None:
        percent_space = np.append(percent_space, percent_credit)
    if lgd_space is None:
        lgd_space = default_lgd_space()

    profits, threshold_space, _ = calc_multi_profits(y_true, y_score, percent_space, lgd_space)
    if ax is None:
        plt.figure(figsize=(7, 7), facecolor='w')
    for percent in percent_space:
        for lgd in lgd_space:
            profit = profits[(percent, lgd)]
            color = plt.plot(threshold_space, profit, label='{}% lgd {}%'.format(float_to_str(percent), float_to_str(lgd)))[0].get_color()
            max_profit = max(profit)
            if max_profit > 0:
                best_profit = threshold_space[profit.argmax()]
                plt.scatter(best_profit, max_profit, color=color, alpha=0.5)
                plt.annotate(f'{np.round(max_profit * 100, 1)}%', (best_profit, max_profit),
                             xytext=(3, 7), textcoords='offset points', ha='center', va='bottom', color=color,
                             bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3))
    if title is None:
        plt.title('Зависимость прибыли от параметра разбиения и процента по кредиту')
    else:
        plt.title(title)
    plt.legend(loc='best')
    plt.grid(True)
    plt.xlabel('Параметр разбиения принадлежности к классу')
    plt.ylabel('Прибыль')
    if y_lim is None:
        plt.ylim([0, 1])
    else:
        plt.ylim(y_lim)
    if x_lim is None:
        plt.xlim([0, 1])
    else:
        plt.xlim(x_lim)


def plt_profit_recall(y_true: np.ndarray, y_score: np.ndarray,
                      ax=None,
                      title=None,
                      percent_space=None,
                      lgd_space=None,
                      plot_roc=True):
    """
    Plot profit rate with respect to recall

    :param y_true: array, shape = [n_samples]
        true binary labels
    :param y_score: array, shape = [n_samples]
        target probabilities
    :param title: str, default None
        The title for plotting
    :param percent_space: array
        percents to plot
    :param lgd_space: array
        lgd to calculate
    :param plot_roc: bool, default True
        Is to plot roc curve
    """
    if percent_space is None:
        percent_space = default_percent_space()
    if lgd_space is None:
        lgd_space = default_lgd_space()
    fpr_, tpr_, threshold_ = roc_curve(y_true, y_score, drop_intermediate=False)
    auc = roc_auc_score(y_true, y_score)
    profits = {}
    for percent in percent_space:
        for lgd in lgd_space:
            profits[(percent, lgd)] = []

    profits, threshold, fpr = calc_multi_profits(y_true, y_score, percent_space, lgd_space)
    if ax is None:
        plt.figure(figsize=(7, 7), facecolor='w')

    if plot_roc:
        plt.plot(fpr_, tpr_, label='ROC AUC={}'.format(float_to_str(auc)))

    plt.plot([0, 1], [0, 1], color='navy', linestyle='--', alpha=0.5)
    for percent in percent_space:
        for lgd in lgd_space:
            color = plt.plot(fpr, profits[(percent, lgd)], label='{}% lgd {}%'.format(float_to_str(percent), float_to_str(lgd)))[0].get_color()
            max_profit = max(profits[(percent, lgd)])
            if max_profit > 0:
                best_profit = fpr[profits[(percent, lgd)].argmax()]
                plt.scatter(best_profit, max_profit, color=color, alpha=0.5)
                plt.annotate(f'{np.round(max_profit * 100, 1)}%', (best_profit, max_profit),
                             xytext=(3, 7), textcoords='offset points', ha='center', va='bottom', color=color,
                             bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3))

    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate/Прибыль')
    plt.title('Зависимость прибыли от Recall' if title is None else title)
    plt.grid(True)
    plt.legend(loc='best')


def plt_mcc(y_true: np.ndarray, y_score: np.ndarray,
            ax=None,
            title=None,
            thresholds=None,
            progress_bar=False):
    """
    Plot MCC with respect to recall

    :param y_true: array, shape = [n_samples]
        true binary labels
    :param y_score: array, shape = [n_samples]
        target probabilities
    :param thresholds: array
        threshold to calculate
    :param progress_bar: bool, default True
        Is to draw progress bar while calculating
    """
    iterator = tqdm_notebook if progress_bar else _empty_iterator
    if thresholds is None:
        thresholds = default_threshold_space()
    mcc = []
    y_true_0 = y_true == 0
    y_true_1 = y_true == 1
    for threshold in iterator(thresholds):
        predict_round = (y_score > threshold).astype(np.uint8)
        eq = predict_round == y_true
        neq = ~eq
        tn = (y_true_0 & eq).mean()
        tp = (y_true_1 & eq).mean()
        fn = (y_true_1 & neq).mean()
        fp = (y_true_0 & neq).mean()
        if (tp + fp == 0) or (tp + fn == 0) or (tn + fp == 0) or (tn + fn == 0):
            thresholds = np.delete(thresholds, threshold)
        else:
            val = (tp * tn - fp * fn) / np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
            mcc.append(val)

    if ax is None:
        plt.figure(figsize=(7, 7), facecolor='w')
    color = plt.plot(thresholds, mcc, label='MCC')[0].get_color()
    max_profit = max(mcc)
    if max_profit > 0:
        plt.scatter(thresholds[mcc.index(max_profit)], max_profit, color=color, alpha=0.5)
        plt.annotate(f'{np.round(max_profit * 100, 1)}%', (thresholds[mcc.index(max_profit)], max_profit),
                     xytext=(3, 7), textcoords='offset points', ha='center', va='bottom', color=color,
                     bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3))
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel('Параметр разбиения принадлежности к классу')
    plt.ylabel('MCC value')
    plt.title('Зависимость метрики MCC от порога разбиения' if title is None else title)
    plt.grid(True)


def plt_popularity(y_score: np.ndarray,
                   ax=None,
                   title=None,
                   thresholds=None,
                   progress_bar=False):
    iterator = tqdm_notebook if progress_bar else _empty_iterator
    if thresholds is None:
        thresholds = default_threshold_space()
    hist = []
    for i in iterator(range(1, len(thresholds))):
        val = (y_score < thresholds[i]).mean()
        hist.append(val)
    if ax is None:
        plt.figure(figsize=(7, 7), facecolor='w')
    plt.plot(thresholds[1:], hist, label=title)
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel('Параметр разбиения принадлежности к классу')
    plt.ylabel('Доля объектов ниже порога')
    plt.title('Распределение объектов по вероятностям' if title is None else title)
    plt.grid(True)


def plt_fp(y_true: np.ndarray, y_score: np.ndarray,
           ax=None,
           title=None,
           thresholds=None,
           progress_bar=False):
    iterator = tqdm_notebook if progress_bar else _empty_iterator
    if thresholds is None:
        thresholds = default_threshold_space()
    result = []
    for threshold in iterator(thresholds):
        predict_round = (y_score > threshold).astype(np.uint8)
        fp = ((y_true == 0) & (predict_round != y_true)).sum()
        right = predict_round.sum()
        result.append(fp / right)

    if ax is None:
        plt.figure(figsize=(7, 7), facecolor='w')
    plt.plot(thresholds, result)
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel('Параметр разбиения принадлежности к классу')
    plt.ylabel('FPR')
    plt.title('Зависимость FPR от порога разбиения' if title is None else title)
    plt.grid(True)
