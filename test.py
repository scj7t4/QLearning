import qlearning
import random
import qupload

#Implement the q learning project from my book with da robot
#& make sure you can upload shit.
def move(dir,c):
    if dir == 0: # Up
        if c in [0,1,2]:
            return (c,-1)
        else:
            k = c-3
            return (k, 0 if k != 0 else 10)
    if dir == 1: # Right
        if c in [2,5,8]:
            return (c,-1)
        else:
            k = c+1
            return (k, 0 if k != 0 else 10)
    if dir == 2: #Down
        if c in [6,7,8]:
            return (c,-1)
        else:
            k = c+3
            return (k, 0 if k != 0 else 10)
    if dir == 3: #Left
        if c in [0,3,6]:
            return (c,-1)
        else:
            k = c-1
            return (k, 0 if k != 0 else 10)
            
def main():
    #The game is easy. The robot will randomly spawn in one of the 9 cells at the start.
    #The robot moves up down left or right to move through the grid (9 states, 4 actions)
    #If it tries to move into a wall, the move is disallowed and robot gets a penalty of -1
    #Moving somewhere gives a reward 0. Moving to 1 gives reward 10.
    Q = qlearning.QLearner(9,4,discount=0.9,stepsize=0.1,T=1000)
    current = random.randint(1,8)
    
    
    for _ in range(5000):
        dir = Q.act(0,current)
        (state,r) = move(dir,current)
        Q.reward(0,r)
        Q.commit(0,state)
        current = state
        if current == 0:
            current = 8
        
    Q.debug()
    with open('trace','w+') as fp:
        Q.pickle_trace(fp)
        qupload.upload('robot',fp)
    
if __name__ == "__main__":
    main()
