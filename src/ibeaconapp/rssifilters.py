import numpy as np
from sklearn.mixture import GaussianMixture

def gmm_filter(values):
    data = np.array(values).reshape(-1,1)

    # fit models with 1-5 components
    N = np.arange(1, 5)
    models = [None for i in range(len(N))]

    for i in range(len(N)):
        gm = GaussianMixture(n_components=N[i], covariance_type='tied', n_init=3)
        models[i] = gm.fit(data)

    # compute the AIC value for each model
    AIC = [m.aic(data) for m in models]

    best_model = models[np.argmin(AIC)]
    filtered_rssi = max(best_model.means_)

    return float(filtered_rssi)