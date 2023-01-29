from collections import deque


class Undo_Redo:
    #Undo/Redo stack using a deque "list" for efficient append and pop operations
    
    def __init__(self):
        #Create empty deck and init index
        self.stack = deque()
        self.index = -1

    def append(self, obj):
        #Append an obj to the Undo/Redo stack
        #If undo has been done before, remove these objects
        self.pop() #Remove objects from current index to end
        #Append new obj to the stack and inc index
        self.stack.append(obj)
        self.index += 1

    def pop(self):
        #Remove all objects from current index+1 to end from stack
        for i in range(self.index + 1, len(self.stack)):
            self.stack.pop()

    def undo(self):
        #UNDO operation 
        #Just left shift the index if possible
        if self.index > 0:
            self.index -= 1

    def redo(self):
        #REDO operation
        #Just right shift the index if possible
        if self.index < (len(self.stack) - 1):
            self.index += 1


    def undo_available(self):
        #Return True if UNDO available
        if self.index > 0:
            return True
        else:
            return False

    def redo_available(self):
        #Return True if REDO available
        if self.index < len(self.stack) - 1:
            return True
        else:
            return False
        
    def current_obj(self):
        #Returns the current obj from the UNDO/REDO stack
        #If no undo operations have been performed, 
        #this is always the right end of the deque
        return self.stack[self.index]
        
