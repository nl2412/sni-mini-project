#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SNI 2019 - file MM1.py
"""
import random
import numpy as np
import sys, getopt
from math import log
import CoreSim as cs

def expo(mean):
    return -mean*log(np.random.random_sample())

arr = 1		# event-class: arrivals
dep = 2		# event-class: departures

if __name__ == "__main__":
    params = sys.argv[1:]
    if len(params) != 5:
        print("\n --- Usage: %s  mtba  mst  T  seed K\n" % sys.argv[0])
        exit(0)
    else:
        mtba = float(sys.argv[1])	# mean time between arrivals
        mst = float(sys.argv[2])		# mean service time
        T = float(sys.argv[3])			# total simulation time
        seed = int(sys.argv[4])		# seed for the pseudo-r.n.
        K = int(sys.argv[5])  # number of customers served
        print("\n --- Data: mtba = %.1f, mst = %.1f, T = %.1f, seed = %d" % (mtba,mst,T,seed))


# --- first operations on the scheduler

EvL = cs.LinkedList(T)	# --- end of simulation at time T

t = expo(mtba)
ev = cs.CREATE_EV(t,arr)
EvL.InsertEv(ev)	# --- first arrival at time t
fifo_list.append(t)

t = t + mst
ev = cs.CREATE_EV(t,dep)
EvL.InsertEv(ev)	# --- first departure at time t

# --- initializing main variables
s = 0.0
nbUnits = 0
t_old = 0.0
t_next_arr = 0.0

nclass = -1
i = 0
R_total = 0 # total response time of all customers
fifo_list = [] # FIFO list queue

### --- central simulation loop
while nclass != cs.END_SIM:

    # if 100 customers have been served
    if i == K:
        meanNbOfUnits = s/t_old # calculate meanNbOfUnits at the virtual time time
        meanDelay= R_total/K # calculate average for first K customers
        break

    time, nclass = EvL.FirstEv()

    # ----------
    if nclass == arr:
        s = s + nbUnits*(time - t_old)
        nbUnits = nbUnits + 1
        t = time + expo(mtba)
        ev = cs.CREATE_EV(t,arr)
        EvL.InsertEv(ev)
        t_next_arr = t

        fifo_list.append(t) # store arrived time of customer to a list (queue)

    # ----------
    elif nclass == dep:
        s = s + nbUnits*(time - t_old)
        nbUnits = nbUnits - 1
        if nbUnits > 0:
            t = time + mst
        else:
            t = t_next_arr + mst
        ev = cs.CREATE_EV(t,dep)
        EvL.InsertEv(ev)

        R_curr = t - fifo_list[0] # calculate reponse time of the leaving customer
        R_total+= R_curr # calculate total response time for all customers that left

        del(fifo_list[0]) # remove customer entry from queue

        i+=1 # increase count by 1 for each customer left

    # ----------
    elif nclass == cs.END_SIM:
        s = s + nbUnits*(T - t_old)
        meanNbOfUnits = s/T
    # ----------
    else:
        print("Error")
    #
    #
    t_old = time
    ### --- central simulation loop

# --- output    
print("\n --- meanNbOfUnits = %f\n" % meanNbOfUnits)
print("\n --- meanDelay = %f\n" % meanDelay)
print("\n --- meanJitter= %f\n" % meanJitter)

        
    