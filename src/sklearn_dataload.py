import os
import numpy as np
from sklearn.model_selection import train_test_split

from vtuber_dataclass import VtuberDataclass, load_vdatas

def data_load(seed=13) -> tuple[np.ndarray]:
    DATA_PATH = os.path.join("data", "vdata_with_variables.json")

    vdatas = load_vdatas(DATA_PATH)
    X = np.array([vd.doc_vec for vd in vdatas])
    Y = np.array([vd.fan_mark_indices[0] for vd in vdatas])

    return train_test_split(X, Y, test_size=0.2, random_state=seed)
