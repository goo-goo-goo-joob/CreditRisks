import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, auc


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


