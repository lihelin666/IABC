import time

def tic():
    globals()['tt'] = time.clock()

def toc():
    print('\nElapsed time: %.8f seconds\n' % (time.clock()-globals()['tt']))
