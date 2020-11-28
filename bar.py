from progress.bar import Bar
import time

def printStatus(info):
    with Bar(info, max=100) as bar:
        for i in range(100):
            # Do some work
            time.sleep(0.01)
            bar.next()

    
