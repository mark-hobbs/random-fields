import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


class RandomField():
    """
    Random field class

    Attributes
    ----------

    Methods
    -------

    Notes
    -----
    """

    def __init__(self, covariance_function, probability_distribution):
        pass

    def generate_normally_distributed_variables(self, array):
        """
        Generate a standard Gaussian random vector

        Parameters
        ----------

        Returns
        -------
        xi : ndarray
            Standard Gaussian random vector
        """
        return np.random.uniform(low=0.0, high=1.0, size=[len(array)])

    def generate_correlated_random_variables(self):
        pass

    def visualise(self, x, K, sz=10):
        """
        Visualise the generated random field
        """
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.scatter(x[:, 0], x[:, 1], s=sz, c=K, marker='o', cmap=cm.jet)
        ax.axis('off')
        plt.axis('scaled')


class KLexpansion(RandomField):
    """
    Karhunen-Loève expansion class

    Attributes
    ----------

    Methods
    -------

    Notes
    -----
    """
    pass


class MatrixDecomposition(RandomField):
    """
    Matrix-decomposition class

    Attributes
    ----------

    Methods
    -------
    build_distribution

    Notes
    -----
    """

    def __init__(self, C, probability_distribution):
        self.C = C
        self.distribution = probability_distribution
        (self.eigenvalues,
         self.eigenvectors) = self.decompose_covariance_matrix()
        self.L = self.compute_lower_triangular_matrix()

    def decompose_covariance_matrix(self):
        """
        Decompose the covariance matrix into its eigenvalues and eigenvectors
        """
        eigenvalues, eigenvectors = np.linalg.eig(self.C)
        return eigenvalues.real, eigenvectors.real

    def compute_lower_triangular_matrix(self):
        """
        Compute the lower triangular matrix

        Parameters
        ----------

        Returns
        -------
        L : ndarray
            Lower triangular matrix
        """
        return np.sqrt(np.absolute(self.eigenvalues)) * self.eigenvectors

    def generate_sample_normal(self):
        """
        Generates a single sample of the random field with a standard normal
        distribution (mean 0 and variance 1)

        Parameters
        ----------

        Returns
        -------
        K : ndarray
            Sample of the random field

        """
        return np.matmul(self.L,
                         self.generate_normally_distributed_variables(self.C))

    def generate_sample(self):
        """
        Generates a single sample of the random field with the user defined
        distribution parameters (mean and standard deviation)

        Parameters
        ----------

        Returns
        -------

        """
        return self.distribution.build(self.generate_sample_normal())

    def generate_samples(self, n_samples):
        """
        Generates multiple samples of the random field with the user defined
        distribution parameters (mean and standard deviation)

        Parameters
        ----------

        Returns
        -------

        """
        samples = np.zeros([len(self.C), n_samples])
        for i in range(n_samples):
            samples[:, i] = self.generate_sample()
        return samples
