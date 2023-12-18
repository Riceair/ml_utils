from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np

base_metrics = {"Accuracy": accuracy_score,
                "Precision": precision_score,
                "Recall": recall_score,
                "F1": f1_score,}

def evalBase(targets, outputs):
    result = dict()
    for key, metric in base_metrics.items():
        if key == "Accuracy":
            score = metric(targets, outputs)
        else:
            score = precision_score(targets, outputs, average="macro")
        result[key] = score
    return result

def diplayConfusion(targets, outputs, labels):
    cm = confusion_matrix(targets, outputs, labels=labels)
    cm_display = ConfusionMatrixDisplay(cm, display_labels=labels)
    cm_display.plot(cmap="Blues")
    plt.show()