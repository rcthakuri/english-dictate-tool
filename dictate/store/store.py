import os
import pickle

STORE_PATH = os.path.abspath('./dictate/store')


class Store:
    def __init__(self):
        self.store_path = STORE_PATH + '/store.pickle'

    def save(self, store_data):
        with open(self.store_path, 'wb') as store_fh:
            pickle.dump(store_data, store_fh)

    def load(self) -> dict or None:
        store_data = None
        if os.path.exists(self.store_path):
            with open(self.store_path, 'rb') as store_fh:
                store_data = pickle.load(store_fh)
        return store_data
