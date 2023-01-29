import json
from copy import deepcopy

class Sudoku():

    def __init__(self):
        #Init the list of list tables for numbers, status and allowed numbers
        #Inner lists are columns
        self.table = list() #Numberes
        self.s_table = list() #Status
        for x in range(9):
            self.table.append([0,0,0,0,0,0,0,0,0])
            self.s_table.append([-1,-1,-1,-1,-1,-1,-1,-1,-1])
                    
        #Variable for generation to set as status
        self.generation = 0
        
        #Diagonal rule
        self.diagonal_rule = False
    
        #Set status const
        self.LOCKED = 0
        self.CAND = -1
        self.WRONG = -2

    def from_json(obj):
        # Factory method to create a new sudoku object from the the json string
        if 'table' in obj and 's_table' in obj and 'generation' in obj:
            s = Sudoku()
            s.table = obj['table']
            s.s_table = obj['s_table']
            s.generation = obj['generation']
        if 'diagonal_rule' in obj:   
            s.diagonal_rule = obj['diagonal_rule']
        return s

    def to_json(self):
        #Create a json string from the current sudoku object
        return json.dumps(self, default=lambda o: vars(o))
        
    def copy(self):
        #Return a copy of the object 
        #(for undo stack)
        return deepcopy(self)
        

    def fill_example(self):
        #Fill example sudoku
        self.sc(1, [5,0,0,0,0,0,0,0,4])
        self.sc(2, [1,0,3,6,0,8,2,0,5])
        self.sc(3, [0,0,0,0,1,0,0,0,0])
        self.sc(4, [0,0,4,3,0,5,8,0,0])
        self.sc(5, [3,0,8,0,0,0,9,0,1])
        self.sc(6, [0,0,2,1,0,9,3,0,0])
        self.sc(7, [0,0,0,0,5,0,0,0,0])
        self.sc(8, [8,0,1,9,0,4,5,0,3])
        self.sc(9, [2,0,0,0,0,0,0,0,9])
        
        
    def __str__(self):
        #Nicely print the grid
        s = str()
        for row in self.table:
            for col in reversed(row):
                s += (str(col) + " ")
            s += ("\n")
        return s

    def sn(self, r, c, number):
        #print("sn {0} at r{1}/c{2}".format(number, r,c))  
        #Increase generation if number > 0
        if number > 0:
            self.generation += 1
        #Set the number at row, column index
        self.table[c-1][9-r] = number    
        #Find the status
        self.fs(r,c)            

    def fs(self, r, c):
        #Find and set the status for a cell
        
        number = self.gn(r,c)#Get current number
        if number == 0:
            #If the number is 0 the cell has the candidate status
            self.ss(r,c, self.CAND)
        if self.gs(r,c) == self.LOCKED:
            return
        #Temporary delete number to get allowed numbers (Only works for empty cells)
        self.table[c-1][9-r] = 0                                
        an = self.an(r,c)
        if number > 0:
            if number in an:
                #Set the cell status as the generation
                self.ss(r,c, self.generation+1)
            else:
                self.ss(r,c, self.WRONG)
                #print("sn wrong {0} at r{1}/c{2}".format(number, r,c))
                
            self.table[c-1][9-r] = number #Reenter the saved number
        else:
            #Empty cell should have at least one an
            if len(an) == 0:
                self.ss(r,c, self.WRONG)
                #print("empty cell at r{0}/c{1} has no an".format(r,c))

    def lock(self, r, c):
        #Lock the number at row, column index
        self.s_table[c-1][9-r] = self.LOCKED

    def unlock(self, r, c):
        #Lock the number at row, column index
        self.s_table[c-1][9-r] = self.CAND


    def ss(self, r, c, status):
        #Set the status at row, column index
        self.s_table[c-1][9-r] = status

    def sc(self, c, l):
        #Fill the column c in the table with column list l
        l.reverse()
        self.table[c-1] = l
        #Also fill the status table with 1 for locked numbers
        self.s_table[c-1] = [self.LOCKED if n > 0 else self.CAND for n in l]

    def get_col(self, c):
        #Get the column c from the table
        l = self.table[c-1]
        f = self.s_table[c-1]
        return list(reversed(l))

    def get_row(self, r):
        #Get the row r from the table
        row = []
        for col, filt in zip(self.table, self.s_table):
            row.append(col[9-r])
        return row
    
    def get_diagonal(self, r, c):
        #Get the numbers in the diagonal crossing the number
        #IF the number is on one of the 2 diagonals
        diagonal1 = []
        diagonal2 = []
        in_diagonal1 = False
        in_diagonal2 = False                
        for col_number, col in enumerate(self.table):
            diagonal1.append(col[col_number])
            diagonal2.append(col[8-col_number])
            if c == col_number + 1:
                if r == col_number + 1:
                    #print("r{0}/c{1} == col_number + 1".format(r,c))                    
                    in_diagonal2 = True
                if r == 9 - col_number:
                    #print("r{0}/c{1} == 9 - col_number".format(r,c))                       
                    in_diagonal1 = True       
        if in_diagonal1 and in_diagonal2:
            #print("Diagonal 1 and" + str(diagonal1))
            #print("Diagonal 2" + str(diagonal2))                    
            diagonal1.extend(diagonal2)            
            return diagonal1
        elif in_diagonal1:
            #print("Diagonal 1 only" + str(diagonal1))                    
            return diagonal1
        elif in_diagonal2:
            #print("Diagonal 2 only" + str(diagonal2))        
            return diagonal2
        else:
            return []
        
        

    def get_block(self, row, col):
        #Get numbers in the block around row, col
        block_corr = self.get_block_corr(row, col)
        #Make list of numbers out of list of block coord. tuples
        return [self.gn(b[0], b[1]) for b in block_corr]

    def an(self, row, col):
        #print("an {0}/{1}".format(row, col))  
        #Get allowed numbers for row col
        n = self.gn(row, col)
        status = self.gs(row, col)
        candidates = set([1,2,3,4,5,6,7,8,9])
        if n > 0:
            #Cell is filled. No allowed numbers
            return []
        else:
            candidates = candidates.difference(self.on(self.get_block(row,col)))
            candidates = candidates.difference(self.on(self.get_row(row)))
            candidates = candidates.difference(self.on(self.get_col(col)))
            if self.diagonal_rule:
                candidates = candidates.difference(self.on(self.get_diagonal(row, col)))
            return list(candidates)

    def get_row_cand(self, r):
        #Get the list of sets of allowed numbers for the row from the table
        row_an = [self.on(self.an(r,c+1)) for c in range(9)]     
        #print("get_row_cand {0} row_an: {1}".format(r, row_an))
        #Make result of returned candidate and tuple with cell corrdinates
        result = [(cand[0], (r, cand[1])) for cand in self.find_cand(row_an)]
        #if len(result)>0:        
            #print("get_row_cand {0} returned: {1}".format(r, result))
        return result


    def get_col_cand(self, c):
        #Get the list of sets of allowed numbers for the col from the table
        col_an = [self.on(self.an(r+1,c)) for r in range(9)]
        
        #return candidate and col_index
        #Make result of returned candidate and tuple with cell corrdinates
        result = [(cand[0], (cand[1], c)) for cand in self.find_cand(col_an)]
        #if len(result)>0:
            #print("get_col_cand {0} returned: {1}".format(c, result))        
        return result
    
    def get_block_cand(self, row, col):
        #Get the list of sets of allowed numbers for the block around r,c
        block_corr = self.get_block_corr(row, col)
        block_an = [self.on(self.an(b[0],b[1])) for b in block_corr]
        #Make result of returned candidate and tuple with cell corrdinates
        result = [(cand[0], block_corr[cand[1]-1]) for cand in self.find_cand(block_an)]
        #if len(result)>0:        
            #print("get_block_cand {0}/{1} returned: {2}".format(row, col, result))        
        return result


    def get_block_corr(self, row, col):
        #Get coord. tuples of block around row, col
        block = []
        #Calc start/stop of for loops so that each will around
        #each 3 rows/col, so each cell in the block
        for c in range(int((col-1)/3)*3, int((col-1)/3)*3 + 3):
            for r in range(int((row-1)/3)*3,int((row-1)/3)*3+3):
                #print("r{0}/c{1}".format(r+1,c+1))
                #Append tuple with row, col
                block.append((r+1,c+1))
        return block

    def find_cand(self, an_list):
        #Find candidates for a number in a list of sets of allowed num.
        #(for row, col or block)
        candidates = []
        #Find cells whith only 1 allowed number
        for ind, s in enumerate(an_list):
            if len(s) == 1:
                #print("find_cand for {0} returned: {1}".format(an_list, ind+1))
                #Use next(iter(s)) to get the element of s without removing it
                candidates.append((next(iter(s)), ind+1))
        
        #Calc occurance of numbers in list
        for n in range(9):
            members = [n+1 in s for  s in an_list]
            #If a number appears in allowed number list of only one cell
            if sum(members) == 1:
                #We found a candidate
                ind = members.index(1)+1
                cand = n+1
                #Append tuple with cand, index
                candidates.append((cand, ind))
        #return candidates list
        return candidates
                
    def gcand(self, row, col):
        #Get the possible candidate for a cell
        candidates = []
        #Collect all candidates
        candidates.extend(self.get_row_cand(row))        
        candidates.extend(self.get_col_cand(col))        
        candidates.extend(self.get_block_cand(row,col))        
        for cand in candidates:
            #Return the first valid candidate
            if len(cand) > 0:        
                if cand[1][0] == row and cand[1][1] == col:
                    return cand[0]
        return 0

    def us(self):
        #Recursively set all unambigous candidates to the grid
        #print("Iterating")        
        candidates = []
        for r in range(1,10):
            #Append row candidates
            candidates.extend(self.get_row_cand(r))
        for c in range(1,10):
            #Append col candidates
            candidates.extend(self.get_col_cand(c)
                              )            
        for r in range(1,10,3):
            for c in range(1,10,3):
                #Append block candidates
                candidates.extend(self.get_block_cand(c,r))
        if len(candidates) == 0:
            #print("Iterating complete")
            return True
        else: 
            for cand in candidates:
                if len(cand) > 0:
                    if self.gn(cand[1][0], cand[1][1]) == 0:
                        #print("Setting {0} at {1}/{2}".format(cand[0], cand[1][0], cand[1][1]))
                        #Set number without calling us() again
                        self.sn(cand[1][0], cand[1][1], cand[0])
                        if self.gs(cand[1][0], cand[1][1]) == self.WRONG:
                            #print("us set a wrong number :D")
                            self.sn(cand[1][0], cand[1][1], 0)
                            #print("Iterating failed")                            
                            return False
            #print("Next generation {0}".format(self.generation+1))
            #Increase the generation
            self.generation += 1               
            #print("Iteration finish")
            return self.us()                                   
        
                
    def on(self, l):
        #Get set > 0 in the provided list
        return set(sorted([n for n in l if n > 0]))

    def gn(self, row, col):
        #Get the number at row r, column c
        return self.table[col-1][9-row]

    def gs(self, row, col):
        #Get the status at row r, column c
        return self.s_table[col-1][9-row]


