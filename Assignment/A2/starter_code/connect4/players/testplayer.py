from connect4.utils import get_pts, get_valid_actions, Integer
import numpy as np
def update_board(state,player_number,action):
        board, num_popout = state
        col,b=action
        empty=-1
        for i in range(len(board)-1,-1,-1):
            if(board[i][col]==0):
                empty=i
                break
        board1=np.copy(board)
        if(b and num_popout[player_number].get_int()>0):
            for j in range(len(board)-1,empty+1,-1):
                board1[j][col]=board1[j-1][col]
            board1[empty+1][col]=0
        elif(not(b)):
                board1[empty][col]=player_number
        else:
            print("Error in action")                 
        return board1
# def get_successors(state,player):
#         board, num_popout = state
#         is_pop=False
#         print(board,num_popout,player)
#         successors=[]
#         empty=[None]*len(board[0])
#         for i in range(len(board[0])):
#             for j in range(len(board)-1,-1,-1):
#                 if(board[j][i]==0):
#                     # print(j,i)
#                     empty[i]=j
#                     break
#         board1=np.copy(board)
#         # make_equal(board1,board)
#         for i in  range(len(empty)):
#             if(empty[i]==None):
#                 continue
#             board1[empty[i]][i]=player
#             successors.append((board1,is_pop))
#             board1=np.copy(board)
#             # make_equal(board1,board)
#         is_pop=True    
#         if(num_popout[player]>0):    
#             for i in range(len(empty)):
#                 if(empty[i]==len(board)-1):
#                     continue
#                 if(i%2==0 and player==2):
#                     continue
#                 if(i%2==1 and player==1):
#                     continue
#                 for j in range(len(board)-1,empty[i]+1,-1):
#                     board1[j][i]=board1[j-1][i]
#                 board1[empty[i]+1][i]=0    
#                 successors.append((board1,is_pop))
#                 board1=np.copy(board)
#         return successors
def get_successors(self,state):
        board, num_popout = state
        actions=self.get_valid_actions(self.player_number,state)
        empty=[None]*len(board[0])
        for i in range(len(board[0])):
            for j in range(len(board)-1,-1,-1):
                if(board[j][i]==0):
                    # print(j,i)
                    empty[i]=j
                    break
        successors=[]        
        for col,b in actions:
            board1=np.copy(board)
            if(b and num_popout>0):
                for j in range(len(board)-1,empty[col]+1,-1):
                    board1[j][col]=board1[j-1][col]
                board1[empty[col]+1][i]=0
            else:
                board1[empty[col]][col]=self.player_number    
            successors.append(board1)
        # print(successors)    
        # return successors        
        print(len(successors),len(successors[0]),len(successors[0][0]))        
        print(successors)
        for i in range(len(successors)):
            for j in range(len(successors[i])):
                for k in range(len(successors[i][j])):
                    print(successors[i][j][k],end=" ")    
                print()
            print()    
            
print(update_board((np.array([[0,0,0,0,0,0], 
[1 ,0, 0, 0, 0, 0],
[1 ,1 ,2 ,0 ,0 ,0],
[2 ,1 ,2 ,1 ,2 ,0]]),[10,10,10]),2,(1,False)))        