import keras
import numpy as np
import pickle
# Get one hot, input (N) x 1 [feature last: int, start from 0]
# todo: numpy.array <- cls: int

def _get_onehot(todo,cls:int=None):
    assert todo.shape[-1] == 1
    if cls is not None:
        num_clas = cls
    else:
        num_clas = np.max(todo)+1
    return keras.utils.to_categorical(todo, num_clas).reshape([-1, num_clas])

# import pickle
# Pickle Save:
# file: str  <- obj: any

def pic_save(file:str, obj):
    with open(file, 'wb') as f:
        pickle.dump(obj, f)

# Pickle Load:
# file: str

def pic_load(file:str):
    with open(file, 'rb') as f:
        return pickle.load(f)