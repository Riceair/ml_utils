import numpy as np

def convertProb2Class(y_probs):
    outputs = []
    n_classes = len(y_probs)
    n_samples = len(y_probs[0])

    for i in range(n_samples):
        probs = [y_probs[ci][i][1] for ci in range(n_classes)]
        output = np.zeros(n_classes)
        output[probs.index(max(probs))] = 1
        outputs.append(output)

    return np.array(outputs)