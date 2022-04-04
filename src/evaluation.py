import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay
import matplotlib
import seaborn as sns
from sklearn.metrics import hamming_loss\
                            , accuracy_score, f1_score, precision_score, recall_score\
                                , label_ranking_average_precision_score\
                                    , multilabel_confusion_matrix, plot_confusion_matrix\
                                        , classification_report

def print_confusion_matrix(confusion_matrix, axes, class_label, class_names, fontsize=8):
    """
    source: https://stackoverflow.com/questions/62722416/plot-confusion-matrix-for-multilabel-classifcation-python
    """
    df_cm = pd.DataFrame(
        confusion_matrix, index=class_names, columns=class_names,
    )

    try:
        heatmap = sns.heatmap(df_cm, annot=True, fmt="d", cbar=False, ax=axes, cmap="plasma")
    except ValueError:
        raise ValueError("Confusion matrix values must be integers.")
    heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=fontsize)
    heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=45, ha='right', fontsize=fontsize)
    axes.set_ylabel('')
    axes.set_xlabel('')
    axes.set_title("" + class_label)




def print_eval(estimator, x, y, xt, yt):
    from sklearn.utils import class_weight
    # Plot ROC Curve
    fig, axs = plt.subplots(2, 5, figsize=(19, 7), sharex=True, sharey=True)
    plt.style.use('ggplot')

    matplotlib.rcParams['legend.fontsize'] = 8

    i = 0
    for row in range(2):
        for col in range(5):
            ax = axs[row][col]
            for j in range(5):
                RocCurveDisplay.from_estimator(estimator.estimators_[i], xt, yt.iloc[:, i]\
                    , ax = ax, name = y.columns[i], sample_weight=class_weight.compute_sample_weight('balanced', yt.iloc[:, i]))
                i += 1
            ax.set(xlabel="", ylabel="")

        # Print the statistics
    y_true = yt
    y_pred = estimator.predict(xt)

    print("*"*50)
    print("Hamming loss: ", hamming_loss(y_true, y_pred))
    # print("Ranked avg precision: ", label_ranking_average_precision_score(y_true, y_pred))
    print("Micro Precision: ", precision_score(y_true, y_pred, average='micro', zero_division=0))
    print("Micro Recall: ", recall_score(y_true, y_pred, average='micro'))
    print("Micro F1 score: ", f1_score(y_true, y_pred, average='micro', zero_division=0))
    print("*"*50)
    # f1_score(y_true, y_pred, average='micro')
    pd.DataFrame(classification_report(y_true, y_pred, target_names = y.columns, output_dict=True))

    fig, ax = plt.subplots(1, 10, figsize=(18, 2), sharex = True, sharey=True)
    
    for axes, cfs_matrix, label in zip(ax.flatten(), multilabel_confusion_matrix(y_true, y_pred), y.columns):
        print_confusion_matrix(cfs_matrix, axes, label, ["0", "1"])

    fig.tight_layout()
    plt.show()


if "__main__" == __name__:
    pass
    
