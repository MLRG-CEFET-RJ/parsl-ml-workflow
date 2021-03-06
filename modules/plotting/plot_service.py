import matplotlib.pyplot as plt
from numpy import histogram2d
from numpy import array
from tabulate import tabulate

from matplotlib.ticker import NullFormatter

from keras.callbacks import TensorBoard


def plot(h, metric, dir='../plot/', show_only=False):
    fig, ax = plt.subplots()
    epochs = range(len(h[metric]))
    ax.plot(epochs, h[metric], c='blue', label='train')
    ax.plot(epochs, h['val_'+metric], c='green', label='val')
    ax.legend()
    plt.title(metric)
    ax.set_xlabel('epochs')

    if show_only:
        plt.show()
    else:
        plt.savefig(dir + metric + '.pdf')


def plot_hm(x, y, dir='../plot/', show_only=False):
    heatmap, xedges, yedges = histogram2d(x, y, bins=500)
    extent = [-0.2, 1.0, -0.2, 1.0]

    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower')

    if show_only:
        plt.show()
    else:
        plt.savefig(dir + 'heatmap.pdf')


def plot_scatter(X, Y, X_val, y_val, X_test, Y_test, preds, dir='../plot/', show_only=False):
    plt.clf()
    plt.suptitle("Infrared X Redshift", color='red')

    plt.subplot(221)
    plt.scatter(X[:, 3], Y)
    plt.title("Treino")

    plt.subplot(222)
    plt.scatter(X_val[:, 3], y_val)
    plt.title("Validacao")

    plt.subplot(223)
    plt.scatter(X_test[:, 3], Y_test)
    plt.title("Teste")

    plt.subplot(224)
    plt.scatter(X_test[:, 3], preds)
    plt.title("Predito")

    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)

    if show_only:
        plt.show()
    else:
        plt.savefig(dir + 'redshift.png')


def plot_scatter_lr(X, Y, real, pred, dir='../plot/', show_only=False):
    plt.clf()
    plt.suptitle("Infrared X Redshift", color='red')

    plt.scatter(X[:, 3], Y, color='black')
    plt.plot(real, pred, color='blue', linewidth=3)

    plt.xticks(())
    plt.yticks(())

    if show_only:
        plt.show()
    else:
        plt.savefig(dir + 'linear_reg.png')


def plot_table(x, y):
    t = tabulate(array([x, y]).T[:50], headers=['Real', 'Predict'], tablefmt='orgtbl')
    print(t)


def plot_table_cf(header, cfs):
    t = tabulate(array([cfs]).T, headers=[header], tablefmt='orgtbl')
    print(t)

def plot_simple_table(data):
    t = tabulate(array([data]).T, tablefmt='orgtbl')
    print(t)

def ann_tensorboard_callback():
    return TensorBoard(log_dir='../board', histogram_freq=0, write_graph=True, write_images=True)


def plot_curves(train_sizes, train_mean, train_std, test_mean, test_std, dir='../plot/', show_only=False):

    plt.figure()
    plt.title("Learning Curves")
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    plt.grid()

    plt.fill_between(train_sizes, train_mean - train_std,
                     train_mean + train_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_mean - test_std,
                     test_mean + test_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")

    if show_only:
        plt.show()
    else:
        plt.savefig(dir + 'curves.png')
