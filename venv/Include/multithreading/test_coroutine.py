from multiprocessing import cpu_count
import numpy as np


def chunks(l, n):
    """Yield successive n-sized chunks from l.
    https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks"""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def test():
    n_workers = cpu_count()
    print("workers: ", n_workers)
    input_data = [i for i in range(200)]
    n_batches = int(200/n_workers)
    for batch_names in chunks(input_data, n_batches):
        print(batch_names)
    # pool = ProcessPoolExecutor(max_workers=n_workers)
    


def generator_test():
    t = np.arange(0, 100)

    yield from t



if __name__ == "__main__":
    # test()
    print(list(generator_test()))