import random
import time
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer


class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        self.start_time=0
        self.activate=False
        # Do the rest of your implementation here
        
    def is_start(self,state):
        board,num_popout=state
        if(self.player_number==2):
            return False
        for i in range(len(board)):
            for j in range(len(board[0])):
                if(board[i][j]!=0):
                    return False    
        return True
    
    def is_terminal(self,state,player):
        if(player==1):
            p=self.player_number
        else:
            if(self.player_number==1):
                p=2
            else:
                p=1
        if(len(get_valid_actions(p,state))==0):
            return True                
        board, num_popout = state
        if(num_popout[p].get_int()>0):
            return False
        for i in range(len(board)):
            for j in range(len(board[0])):
                if(board[i][j]==0):
                    return False
        return True        
    
    def update_board(self,state,action,player):
        board, num_popout = state
        col,b=action
        empty=-1
        for i in range(len(board)-1,-1,-1):
            if(board[i][col]==0):
                empty=i
                break
        board1=np.copy(board)
        if(b and num_popout[player].get_int()>0):
            for j in range(len(board)-1,empty+1,-1):
                board1[j][col]=board1[j-1][col]
            board1[empty+1][col]=0
        elif(not(b)):
                board1[empty][col]=player
        else:
            print("Error in action")                 
        return board1            
    
    def expect_utility(self,state,depth,m,time_left):
        board, num_popout = state
        if(time_left<0.0001 or self.time-(time.time()-self.start_time)<0.1):
            if(self.player_number==1):
                return get_pts(self.player_number,board)-get_pts(2,board)
            else:
                return get_pts(self.player_number,board)-get_pts(1,board)
        if(m==0):
            if self.is_terminal(state,0) or depth==0:
                # return get_pts(self.player_number,board)
                if(self.player_number==1):
                    return get_pts(self.player_number,board)-get_pts(2,board)
                else:
                    return get_pts(self.player_number,board)-get_pts(1,board)
            if(self.player_number==1):
                other_player=2
            else:
                other_player=1         
            actions=get_valid_actions(other_player,state)
            utility=0
            cnt=0        
            for i in range(len(actions)):
                tl=time_left/len(actions)
                col,b=actions[i]
                board1=self.update_board(state,actions[i],other_player)
                if(b and num_popout[other_player].get_int()>0):
                    num_popout[other_player].decrement()
                    state1=board1,num_popout
                    utility=utility+self.expect_utility(state1,depth-1,1,tl)
                    cnt=cnt+1
                    num_popout[other_player].increment()
                else:
                    state1=board1,num_popout
                    utility=utility+self.expect_utility(state1,depth-1,1,tl)
                    cnt=cnt+1                            
            if(cnt==0):
                # print("cnt")
                return 0             
            return utility/cnt        
        else:
            if self.is_terminal(state,1) or depth==0:
                # return get_pts(self.player_number,board)
                if(self.player_number==1):
                    return get_pts(self.player_number,board)-get_pts(2,board)
                else:
                    return get_pts(self.player_number,board)-get_pts(1,board)
            actions=get_valid_actions(self.player_number,state)
            # state1=board1,num_popout
            utility=-np.inf
            cnt=0        
            for i in range(len(actions)):
                tl=time_left/len(actions)
                col,b=actions[i]
                board1=self.update_board(state,actions[i],self.player_number)
                if(b  and num_popout[self.player_number]):
                    num_popout[self.player_number].decrement()
                    state1=board1,num_popout
                    utility=max(utility,self.expect_utility(state1,depth-1,0,tl))
                    num_popout[self.player_number].increment()
                else:
                    state1=board1,num_popout
                    utility=max(utility,self.expect_utility(state1,depth-1,0,tl))                    
            return utility
             
    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        self.start_time=time.time()
        board, num_popout = state
        
        actions=get_valid_actions(self.player_number,state)
        
        depth=15
        utility=0
        index=0        
        for i in range(len(actions)):
            time_left=self.time/len(actions)
            col,b=actions[i]
            board1=self.update_board(state,actions[i],self.player_number)
            if(b and num_popout[self.player_number].get_int()>0):
                num_popout[self.player_number].decrement()
                state1=board1,num_popout
                u=self.expect_utility(state1,depth,0,time_left)
                if(u>utility):
                    utility=u
                    index=i
                num_popout[self.player_number].increment()
            else:
                # try:
                state1=board1,num_popout
                u=self.expect_utility(state1,depth,0,time_left)
                if(u>utility):
                    utility=u
                    index=i
                # except:
                #     continue             
        return actions[index]
        
    def max_value(self,state, alpha, beta,depth,time_left):
        # print("min",depth)
        board,num_popout=state
        if(time_left<0.00002 or self.time-(time.time()-self.start_time)<0.1):
            if(self.player_number==1):
                return get_pts(self.player_number,board)-get_pts(2,board)
            else:
                return get_pts(self.player_number,board)-get_pts(1,board)
        
        if self.is_terminal(state,1) or depth==0:
            # return get_pts(self.player_number,board)
            if(self.player_number==1):
                return get_pts(self.player_number,board)-get_pts(2,board)
            else:
                return get_pts(self.player_number,board)-get_pts(1,board)
        v = -np.inf
        for a in get_valid_actions(self.player_number,state):
            t=time_left/len(get_valid_actions(self.player_number,state))
            action,b=a
            board1=self.update_board(state,a,self.player_number)
            # print("max",board1)
            if(b and num_popout[self.player_number].get_int()>0):
                num_popout[self.player_number].decrement()
                state1=board1,num_popout
                v = max(v, self.min_value(state1, alpha, beta,depth-1,t))
                num_popout[self.player_number].increment()
            else:
                state1=board1,num_popout
                v = max(v, self.min_value(state1, alpha, beta,depth-1,t))
            if v >= beta:
                return v 
            alpha = max(alpha, v )
        return v 

    def min_value(self,state, alpha, beta,depth,time_left):
        # print("max",depth)
        board,num_popout=state
        if(time_left<0.00002 or self.time-(time.time()-self.start_time)<0.1):
            if(self.player_number==1):
                return get_pts(self.player_number,board)-get_pts(2,board)
            else:
                return get_pts(self.player_number,board)-get_pts(1,board)
        if self.is_terminal(state,0) or depth==0:
            # return get_pts(self.player_number,board)
            if(self.player_number==1):
                return get_pts(self.player_number,board)-get_pts(2,board)
            else:
                return get_pts(self.player_number,board)-get_pts(1,board)
        v = np.inf
        if(self.player_number==1):
            other_player=2
        else:
            other_player=1    
        for a in get_valid_actions(other_player,state):
            action,b=a
            t=time_left/len(get_valid_actions(other_player,state))
            board1=self.update_board(state,a,other_player)
            # print("min",board1)
            if(b and num_popout[other_player].get_int()>0):
                num_popout[other_player].decrement()
                state1=board1,num_popout
                v = min(v, self.max_value(state1, alpha, beta,depth-1,t))
                num_popout[other_player].increment()
            else:
                state1=board1,num_popout
                v = min(v, self.max_value(state1, alpha, beta,depth-1,t))
            if v <= alpha:
                return v 
            beta = min(beta, v )
        return v        
                                     
                                                 
    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        
        self.start_time=time.time()
        # if(self.player_number==1):
        #     return self.get_expectimax_move(state)   
        board, num_popout = state
        # if(self.is_start(state)):
        #     c=len(board[0])/2-1
        #     b=False
        #     return c,b
        actions=get_valid_actions(self.player_number,state)
        depth=15
        utility=-np.inf
        index=-1
                
        for i in range(len(actions)):            
            time_left=self.time/len(actions)
            col,b=actions[i]
            board1=np.copy(board)
            board1=self.update_board(state,actions[i],self.player_number)
            if(b and num_popout[self.player_number].get_int()>0):             
                num_popout[self.player_number].decrement()
                state1=board1,num_popout
                u=self.min_value(state1,utility,np.inf,depth,time_left)
                if(u>utility):
                    utility=u
                    index=i
                num_popout[self.player_number].increment()
            else:
                state1=board1,num_popout
                u=self.min_value(state1,utility,np.inf,depth,time_left)
                if(u>utility):
                    utility=u
                    index=i     
        return actions[index]