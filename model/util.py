import numpy as np
import matplotlib.pyplot as plt


def plot_evolution_track(path, track):
    y = np.array(track)
    x = np.arange(0, y.shape[0], 1)

    plt.plot(x, y)
    plt.xlabel('Iterations')
    plt.ylabel('MinMax evaluation')
    plt.title('MinMax evaluation per iterations')
    plt.savefig(path)
    plt.clf()
    plt.close()
