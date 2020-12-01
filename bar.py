from progress.bar import Bar
import time
from tqdm import tqdm


def printStatus(info):
    with Bar(info, max=100) as bar:
        for i in range(100):
            # Do some work
            time.sleep(0.01)
            bar.next()

def another():
    pbar = tqdm(["a", "b", "c", "d"])
    for char in pbar:
        time.sleep(0.25)
        pbar.set_description("Processing %s" % char)

def printbar():
    with tqdm(total=100) as pbar:
        for i in range(10):
            time.sleep(0.1)
            pbar.update(10)


# printStatus("info")
# printbar()
if __name__ == "__main__":
    another()

