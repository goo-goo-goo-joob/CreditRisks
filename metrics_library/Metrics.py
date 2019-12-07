import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, auc
from tqdm import tqdm_notebook


def plt_roc(y_true, y_score, alg_name=None):
    """
    Draws receiver operating characteristic curve
    and counts area under curve

    :param y_true:
        True binary labels
    :type y_true: ``array, shape = [n_samples]``
    :param y_score:
        Target scores, probability estimates of the positive class
    :type y_score: ``array, shape = [n_samples]``
    :param alg_name:
        The name of an algorithm to print in title
    :type alg_name: ``str``
    """
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auc1 = roc_auc_score(y_true, y_score)
    plt.figure(figsize=(14, 7))
    if alg_name is None:
        plt.plot(fpr, tpr, label='ROC-AUC: {}'.format(np.round(auc1, 4)))
        plt.title('ROC curve')
    else:
        plt.plot(fpr, tpr, label='{} ROC-AUC: {}'.format(alg_name, np.round(auc1, 4)))
        plt.title('{} ROC curve'.format(alg_name))
    plt.legend(loc='best')
    plt.grid()
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--', alpha=0.5)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.ylim([0, 1.05])
    plt.xlim([0, 1])
    plt.show()


def plt_pr(y_true, y_score, alg_name=None):
    """
    Draws precision recall curve
    and counts area under curve

    :param y_true:
        True binary labels
    :type y_true: ``array, shape = [n_samples]``
    :param y_score:
        Target scores, probability estimates of the positive class
    :type y_score: ``array, shape = [n_samples]``
    :param alg_name:
        The name of an algorithm to print in title
    :type alg_name: ``str``
    """
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    plt.figure(figsize=(14, 7))
    if alg_name is None:
        plt.plot(precision, recall, label='PR-AUC: {}'.format(np.round(auc(recall, precision), 4)))
        plt.title('Precision recall curve')
    else:
        plt.plot(precision, recall, label='{} PR-AUC: {}'.format(alg_name, np.round(auc(recall, precision), 4)))
        plt.title('{} Precision recall curve'.format(alg_name))
    plt.legend(loc='best')
    plt.grid()
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0, 1.05])
    plt.xlim([0, 1])
    plt.show()


def plt_profit(y_true, y_score, alg_name=None, percent_credit=None, y_lim=None,
               percent_space=None, threshold_space=None, log_scale=True):
    """Draws metrics based on profit from credit to bank,
    taking the values of threshold and interest on credit.

    Parameters
    ----------
    y_true : array, shape = [n_samples]
        True binary labels
    y_score : array, shape = [n_samples]
        Target scores, probability estimates of the positive class
    alg_name : str
        The name of the algorithm to print on the title
    percent_credit : float > 0 and <= 1, optional
        If not None, adds a graph corresponding to this parameter
    y_lim : array, shape = [2]
        The limits of graph by y-axis
    percent_space : array, shape = [>=1]
        The values of interest on credit to plot on graph
    threshold_space : array, shape = [>1]
        The increasing values of threshold to plot different ones
    :param log_scale: bool, default True
            plot y axis in log scale
    """
    if percent_space is None:
        percent_space = np.linspace(0.05, 0.5, num=10)
    if percent_credit is not None:
        percent_space = np.append(percent_space, percent_credit)
    if threshold_space is None:
        threshold_space = np.linspace(0.1, 0.5, num=70)
    negative_count = (y_true == 0).sum()
    percent_profits = {k: [] for k in percent_space}
    plt.figure(figsize=(14, 7))
    for threshold in threshold_space:
        predict_round = (y_score > threshold).astype(np.uint8)
        # Others params does not calculated because it is useless
        tn = ((y_true == 0) & (predict_round == y_true)).sum()
        fn = ((y_true == 1) & (predict_round != y_true)).sum()
        for percent in percent_space:
            actual_profit = (percent * tn - fn) / (percent * negative_count)
            percent_profits[percent].append(actual_profit)
    for percent, profit in percent_profits.items():
        color = plt.plot(threshold_space, profit, label='{}%'.format(np.round(percent * 100)))[0].get_color()
        max_profit = max(profit)
        if max_profit > 0:
            plt.scatter(threshold_space[profit.index(max_profit)], max_profit, color=color, alpha=0.5)
            plt.annotate(f'{np.round(max_profit * 100, 1)}%', (threshold_space[profit.index(max_profit)], max_profit),
                         xytext=(3, 7), textcoords='offset points', ha='center', va='bottom', color=color,
                         bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3))
    if log_scale:
        plt.yscale('log', nonposy='clip')
    if alg_name is None:
        plt.title('Зависимость прибыли от параметра разбиения и процента по кредиту')
    else:
        plt.title('{} Зависимость прибыли от параметра разбиения и процента по кредиту'.format(alg_name))
    plt.legend(loc='best')
    plt.grid()
    plt.xlabel('Параметр разбиения принадлежности к классу')
    plt.ylabel('Прибыль')
    if y_lim is None:
        if log_scale:
            plt.ylim([0.0001, 1.5])
        else:
            plt.ylim([0, 1])
    else:
        plt.ylim(y_lim)
    plt.xlim([threshold_space[0], threshold_space[-1]])
    plt.show()


def _empty_iterator(seq):
    for el in seq:
        yield el


def plt_profit_recall(y_true: np.ndarray, y_score: np.ndarray,
                      alg_name=None,
                      percent_space=None,
                      plot_roc=True,
                      points_count=100,
                      progress_bar=True):
    """
    Plot profit rate with respect to recall

    :param y_true: array, shape = [n_samples]
        true binary labels
    :param y_score: array, shape = [n_samples]
        target probabilities
    :param alg_name: str, default None
        algorithm name for plotting
    :param percent_space: array
        percents to plot
    :param plot_roc: bool, default True
        Is to plot roc curve
    :param points_count: int, default 100
        number of points for calculation
    :param progress_bar: bool, default True
        Is to draw progress bar while calculating
    """
    if percent_space is None:
        percent_space = np.linspace(0.05, 0.3, num=6)
    iterator = tqdm_notebook if progress_bar else _empty_iterator
    fpr_, tpr_, threshold = roc_curve(y_true, y_score)
    step = round(len(threshold) / points_count)
    fpr = []
    profits = {k: [] for k in percent_space}
    p = y_true.sum()
    n = len(y_true) - p
    for threshold in iterator(threshold[::step]):
        predict_round = (y_score > threshold).astype(np.uint8)
        tn = ((y_true == 0) & (predict_round == y_true)).sum()
        fp = ((y_true == 0) & (predict_round != y_true)).sum()
        fn = ((y_true == 1) & (predict_round != y_true)).sum()

        fpr.append(fp / n)

        for percent in percent_space:
            actual_profit = (percent * tn - fn) / (percent * n)
            profits[percent].append(actual_profit)
    plt.figure(figsize=(7, 7))

    if plot_roc:
        plt.plot(fpr_, tpr_, label='ROC')

    plt.plot([0, 1], [0, 1], color='navy', linestyle='--', alpha=0.5)
    for percent in percent_space:
        plt.plot(fpr, profits[percent], label='{}%'.format(np.round(percent * 100)))

    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate/Profit')
    plt.title('{} Зависимость прибыли от Recall'.format(alg_name if alg_name is not None else ''))
    plt.grid()
    plt.legend(loc='best')
