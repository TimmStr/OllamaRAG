import os

import kagglehub


def load_kaggle_dataset(dataset="rohitgrewal/restaurant-sales-data"):
    return os.path.join(kagglehub.dataset_download(dataset), os.path.basename(dataset).replace("-", "_") + ".csv")
