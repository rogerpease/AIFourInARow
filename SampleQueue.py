#!/usr/bin/env python3 

import numpy as np

class SampleQueue(object):

  def __init__(self,max_memory=100):
    self.memory = list()
    self.max_memory = max_memory
   
  def remember(self,inputs,outputs):
    self.memory.append([inputs,outputs]) 
    if len(self.memory) > self.max_memory:
      del self.memory[0]
     
  def getlast(self):
    print ("LSM",len(self.memory))
    return self.memory[-1]

  def updatelast(self,inputs,outputs):
    self.memory[-1] = [inputs,outputs]

  def get_batch(self,batch_size=10):
    len_memory  = len(self.memory)
    num_inputs  = self.memory[-1][0].shape[2]
    num_outputs = self.memory[-1][1].shape[2]
     
    inputs  = np.zeros((min(len_memory,batch_size),1,num_inputs)) 
    targets = np.zeros((min(len_memory,batch_size),1,num_outputs)) 

    for i,idx in enumerate(np.random.randint(0,len_memory,size=min(len_memory,batch_size))):
      print(self.memory[idx][0])  
      print(inputs) 
      inputs[i] = self.memory[idx][0]  
      print(self.memory[idx][1])  
      targets[i] = self.memory[idx][1]
    return inputs, targets 

if __name__ == "__main__":
  a = SampleQueue(max_memory=10)
  a.remember(np.array([1,2,3,4]).reshape(1,1,4)  ,np.array([10]).reshape(1,1,1)) 
  a.remember(np.array([1,2,3,4]).reshape(1,1,4)*2,np.array([20]).reshape(1,1,1)*2) 
  aprime,bprime = a.getlast()
  assert(aprime[0][0][0]==2)
  aprime = a.updatelast(np.array([3,6,9,12]).reshape(1,1,4),np.array([30]).reshape(1,1,1))
  aprime,bprime = a.getlast()
  assert(aprime[0][0][1]==6)

  b,c  = a.get_batch(batch_size=2) 
  assert len(b) == 2 
  assert len(c) == 2 

 
