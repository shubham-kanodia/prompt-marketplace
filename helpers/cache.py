import os
import pickle


class CacheHelper:
    def __init__(self, cache_name="new-cache"):
        self.cache_name = cache_name
        if os.path.exists(f"data/{cache_name}"):
            pass
        else:
            os.mkdir(f"data/{cache_name}")

    def add_object(self, obj, name):
        with open(f"data/{self.cache_name}/{name}.pkl", "wb") as fl:
            pickle.dump(obj, fl)

    def get_object(self, name):
        try:
            with open(f"data/{self.cache_name}/{name}.pkl", "rb") as fl:
                obj = pickle.load(fl)
            return obj
        except Exception as exp:
            return None
