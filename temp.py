'''
Created on Mar 22, 2015

@author: kkamath
'''
import multiprocessing
from multiprocessing import Process, Manager

def worker(procnum, return_dict):
    '''worker function'''
#     print str(procnum) + ' represent!'
    return_dict[procnum] = procnum


if __name__ == '__main__':
    manager = Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(1000):
        p = multiprocessing.Process(target=worker, args=(i,return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs: proc.join()
    print return_dict.values()

# def worker(num):
#     """thread worker function"""
# #     print 'Worker:', num
#     return num
# 
# if __name__ == '__main__':
#     jobs = []
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i,))
#         jobs.append(p)
#         p.start()
#         print p.get()