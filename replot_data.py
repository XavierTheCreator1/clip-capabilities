import argparse
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay

from create_embeddings import EMOTIONS

parser = argparse.ArgumentParser(description='Replot the model data')
parser.add_argument('--file', '-f', type=str, help='The file containing the model data', required=True)
parser.add_argument('--no_cm', '-c', help="Opt out of displaying the model's confusion matrices", action=argparse.BooleanOptionalAction)
parser.add_argument('--no_loss_curve', '-l', help="Opt out of displaying the model's loss curve", action=argparse.BooleanOptionalAction)
parser.add_argument('--use_current_date', '-d', help="Use the current data as the first three values in file specification", action=argparse.BooleanOptionalAction)
ARGS = parser.parse_args()

if ARGS.use_current_date:
    FILE = f"{time.strftime('%Y-%m-%d')}-{ARGS.file}"
else:
    FILE = ARGS.file

def plot_loss_curve(data_file):

    # Load the loss curve data
    data = np.load(data_file / "loss_curve.npz")
    loss_curve = data['loss_curve']

    # Plot the loss curve
    plt.plot(loss_curve)
    plt.title('Loss Curve')
    plt.xlabel('Iteration')
    plt.ylabel('Loss')

def plot_cm(data_file):

    # Load the confusion matrix data
    data = np.load(data_file / "confusion_matrices.npz")
    train_cm = data['train_cm']
    test_cm = data['test_cm']

    # Plot the training confusion matrix
    cm_display = ConfusionMatrixDisplay(train_cm, display_labels=EMOTIONS)
    _, ax = plt.subplots()
    cm_display.plot(ax=ax)
    ax.set_title("Training Data Confusion Matrix")

    # Plot the testing confusion matrix
    cm_display = ConfusionMatrixDisplay(test_cm, display_labels=EMOTIONS)
    _, ax = plt.subplots()
    cm_display.plot(ax=ax)
    ax.set_title("Testing Data Confusion Matrix")

if __name__ == '__main__':

    # Check for existence of the file
    FILE_DIR = Path('output') / FILE
    if not FILE_DIR.is_dir():
        raise ValueError(f'File {str(FILE_DIR)} does not exist')

    # Plot the data
    if not ARGS.no_loss_curve:
        plot_loss_curve(FILE_DIR)
    if not ARGS.no_cm:
        plot_cm(FILE_DIR)

    plt.show()