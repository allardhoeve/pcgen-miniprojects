#!/usr/bin/env python
"""
Distribution plot options
=========================
"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

sns.set(style="white")

matplotlib.use("pdf")

rs = np.random.RandomState(9)
mean = [0, 0]
cov = [(1, 0), (0, 2)]
x, y = rs.multivariate_normal(mean, cov, 100).T

color = sns.color_palette()[1]
grid = sns.JointGrid(x, y, space=0, size=6, ratio=50)
grid.plot_joint(plt.scatter, color=color, alpha=.8)
grid.plot_marginals(sns.rugplot, color=color)

grid.savefig("asdf.pdf")
