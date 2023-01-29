import os, sys, json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QDialog, QStatusBar, QLineEdit
from PyQt5.QtCore import Qt
from SudokuMain import Sudoku
from SudokuUndo import Undo_Redo

class Tile(QtWidgets.QWidget):

    activated = QtCore.pyqtSignal(int, int)
    
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.number = 0
        self.candidate = 0
        self.a_numbers = []
        self.locked = False
        self.active = False
        self.n_fontsize = 14
        self.an_fontsize = 9
        self.wrong_number = False
        

    def activate(self):
        if not self.active:
            self.active = True
            self.update()

    def deactivate(self):
        if self.active:
            self.active = False
            self.update()

    def set_number(self, n):
        self.number = n
        self.update()

    def set_candidate(self, n):
        self.candidate = n
        self.update()

    def clear_number(self):
        self.number = 0
        self.update()

    def lock(self):
        self.locked=True
        self.update()

    def unlock(self):
        self.locked = False
        self.update()

    def set_an(self, an):
        self.a_numbers = an
        self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.activated.emit(self.x,self.y)


    def set_font_Sizes(self, available_width):
        if available_width < 40:
            self.n_fontsize = 14
            self.an_fontsize = 0
            self.setContentsMargins(3,3,3,3)            
        elif available_width < 60:
            self.n_fontsize = 24
            self.an_fontsize = 8
            self.setContentsMargins(5,5,5,5)                           
        elif available_width < 70:
            self.n_fontsize = 32
            self.an_fontsize = 10
            self.setContentsMargins(8,8,8,8)                           
        else:
            self.n_fontsize = 40
            self.an_fontsize = 12
            self.setContentsMargins(8,8,8,8)                                
        
            
    def paintEvent(self, e):
        super().paintEvent(e)
        p = QtGui.QPainter(self)
        r = e.rect()
        #Calc font_size and contents margins
        self.set_font_Sizes(e.rect().height())
        wrong = self.wrong_number
        #Draw number if > 0
        if self.number > 0:
            if self.locked:
                pen = QtGui.QPen(Qt.black)
            elif wrong:
                pen = QtGui.QPen(Qt.red)
            else:
                pen = QtGui.QPen(Qt.darkGray)
            p.setPen(pen)            
            f = p.font()
            f.setPointSize(self.n_fontsize)            

            f.setBold(True)
            p.setFont(f)
            p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.number))            
        else:
            if wrong:
            #Draw red background if empty and wrong                
            
                p.setPen(Qt.NoPen)                        
                p.setBrush(QtGui.QBrush(QtGui.QColor("lightcoral")))
                p.drawRect(1,1, r.width()-2, r.height()-2)
            else:
            #Draw candidate if > 0
                if self.candidate > 0:
                    pen = QtGui.QPen(QtGui.QColor("skyblue"))     
                    p.setPen(pen)                                      
                    f = p.font()
                    f.setPointSize(self.n_fontsize)            
        
                    p.setFont(f)
                    p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.candidate))                      
                    

        if self.an_fontsize > 0 and len(self.a_numbers) > 0:
            #Draw allowed number if any and enough space
            f = p.font()
            pen = QtGui.QPen(Qt.black)
            p.setPen(pen)            
            f.setPointSize(self.an_fontsize)
            p.setFont(f)
            if len(self.a_numbers) < 6:
                sl = [str(n) for n in self.a_numbers]
                p.drawText(r, Qt.AlignHCenter | Qt.AlignBottom, ' '.join(sl))
            else:
                st = [str(n) for n in self.a_numbers[:int(len(self.a_numbers)/2)]]
                p.drawText(r, Qt.AlignHCenter | Qt.AlignTop, ' '.join(st))
                sb = [str(n) for n in self.a_numbers[int(len(self.a_numbers)/2):]]
                p.drawText(r, Qt.AlignHCenter | Qt.AlignBottom, ' '.join(sb))
        
        #Draw red frame if active            
        if self.active:
            pen = QtGui.QPen(Qt.red)
            pen.setWidth(2)
            p.setPen(pen)
            p.drawRect(1,1, r.width()-2, r.height()-2)
            
class Grid(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        #Make the grid expandable respecting the minimum size
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                           QtWidgets.QSizePolicy.MinimumExpanding)
        #Create the visible border around the frame
        self.setFrameStyle(self.Box|self.Plain)
        self.setLineWidth(3)


    def sizeHint(self):
        #Size hint for the minimum size
        return QtCore.QSize(630,630)


    def resizeEvent(self, e):
        #When the frame is manually resized maintain the 1:1 aspect ratio
        new_size = QtCore.QSize(10,10)
        #Scale the base size to the new size
        new_size.scale(e.size(), QtCore.Qt.KeepAspectRatio)
        #Resize to 1:1 aspect ratio
        self.resize(new_size)
    
    def paintEvent(self, e):
        #Draw the sudoku grid
        super().paintEvent(e)
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("black"))

        height = painter.device().height() - 4
        width = painter.device().width() - 4
        #Hor. lines
        for y in range(1,9):
            if y%3 == 0:
                pen.setWidth(3)
            else:
                pen.setWidth(1)
            painter.setPen(pen)                
            painter.drawLine(0, int(y*(height/9)+2), width, int(y*(height/9)+2))
        #Vert. lines
        for x in range(1,9):
            if x%3 == 0:
                pen.setWidth(3)
            else:
                pen.setWidth(1)
            painter.setPen(pen)                
            painter.drawLine(int(x*(width/9)+2), 0, int(x*(width/9)+2), height)
        
        
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        
        #Max tries for the solver
        self.MAX_TRIES = 5000
        #Max solutionf for the solver
        self.MAX_SOLUTIONS = 2000
        

        #Central widget with a horizontal layout
        widget = QtWidgets.QWidget()
        parent_layout = QtWidgets.QHBoxLayout()
        widget.setLayout(parent_layout)
        self.setCentralWidget(widget)
        
        #Create the sudoku grid widget and place in the parent layout
        self.grid_frame = Grid()
        parent_layout.addWidget(self.grid_frame)
        #Allow that the grid gets focus, so we can use the cursor keys
        self.grid_frame.setFocusPolicy(QtCore.Qt.StrongFocus)


        #Create a widget for the buttons with a vertical layout
        button_group = QtWidgets.QWidget()
        button_layout= QtWidgets.QVBoxLayout()        
        button_group.setLayout(button_layout)

        #Add buttons for undo/redo, lock, solve and reset               
        self.undo_button = QtWidgets.QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo_action) 
        self.undo_button.setShortcut(QtGui.QKeySequence.Undo)                     
        self.redo_button = QtWidgets.QPushButton("Redo")
        self.redo_button.clicked.connect(self.redo_action)                        
        self.redo_button.setShortcut(QtGui.QKeySequence.Redo)           
        self.lock_button = QtWidgets.QPushButton("Lock")
        self.lock_button.clicked.connect(self.lock_action)        
        self.iterate_button = QtWidgets.QPushButton("Iterate")
        self.iterate_button.clicked.connect(self.iterate_action)
        self.solve_button = QtWidgets.QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_action)        
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_action)
        self.next_button = QtWidgets.QPushButton("Next Solution")
        self.next_button.clicked.connect(self.next_solution_action)             
        

        #Add label for generation
        label_group = QtWidgets.QWidget()

        label_layout= QtWidgets.QVBoxLayout(label_group)  


        self.gen_label = QtWidgets.QLabel("Generation")


        self.input_soduku = QtWidgets.QLineEdit() 
        self.input_soduku.textChanged.connect(self.textchanged) # 监听修改

        # Generate from String
        self.gen_label.setMaximumHeight(20)
        self.gen_display = QtWidgets.QLabel("0")
        self.gen_display.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Raised)
        self.gen_display.setMaximumHeight(20)
        label_layout.addWidget(self.gen_label)        
        label_layout.addWidget(self.gen_display) 
        label_layout.addWidget(self.input_soduku)        

        
        
        #Add the buttons to the widget
        button_layout.addWidget(self.undo_button)        
        button_layout.addWidget(self.redo_button)                
        button_layout.addWidget(label_group)
        button_layout.addWidget(self.lock_button)        
        button_layout.addWidget(self.iterate_button)
        button_layout.addWidget(self.solve_button)        
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.next_button)        

        #Add diagonal rule checkbox
        self.diagonal_checkbox = QtWidgets.QCheckBox("Diagonal rule")
        self.diagonal_checkbox.stateChanged.connect(self.set_diagonal_rule)
        button_layout.addWidget(self.diagonal_checkbox)
        
        #Add show candidate checkbox
        self.candidate_checkbox = QtWidgets.QCheckBox("Show candidates")
        self.candidate_checkbox.stateChanged.connect(self.update_display)        
        button_layout.addWidget(self.candidate_checkbox)        


        button_layout.addStretch()        

        #Add the menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        new_action = QtWidgets.QAction("&New", self)
        new_action.setShortcut(QtGui.QKeySequence.New)        
        new_action.triggered.connect(self.new_action)
        file_menu.addAction(new_action)
        
        load_action = QtWidgets.QAction("&Open", self)
        load_action.setShortcut(QtGui.QKeySequence.Open)        
        load_action.triggered.connect(self.load_action)
        file_menu.addAction(load_action)
        
        save_action = QtWidgets.QAction("&Save", self)
        save_action.setShortcut(QtGui.QKeySequence.Save)
        save_action.triggered.connect(self.save_action)
        file_menu.addAction(save_action)        
        
        #Place the button layout right of sudoku grid
        parent_layout.addWidget(button_group)

        #Create the grid layout for the sudoku grid
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setContentsMargins(0,0,0,0)
        grid_layout.setSpacing(0)
        self.grid_frame.setLayout(grid_layout)  
        
        #Add a statusbar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)              

        #Prepare the grid of tiles (list of lists)
        self.tile_grid = []
        for x in range(9):
            column = []
            for y in range(9):
                #Create a tile and add to the grid layout
                tile = Tile(x,y)
                grid_layout.addWidget(tile, y, x)
                #Also add to the list
                column.append(tile)
                #Connect to the activated signal (Mouse click
                tile.activated.connect(self.toggle_activate_tile)
            self.tile_grid.append(column)
        
        #Prepare empty sudoku
        self.new_action()
        self.show()


    def toggle_activate_tile(self,x,y):
        #This is called by a mouse click in a tile
        #Iterate through all tiles in the grid
        #Activated the clicked tile
        #(if not already active. Then deactivate it)
        #Deactivate all other tiles
        for column in self.tile_grid:
            for tile in column:
                if tile.x == x and tile.y ==y:
                    if not tile.active:
                        tile.activate()
                        #Remember the activated tile
                        self.active_x = x
                        self.active_y = y
                        self.tile_active = True
                    else:
                        tile.deactivate()
                        self.tile_active = False
                else:
                    tile.deactivate()
                

    
        
    def keyPressEvent(self, e):
        #Change the active tile
        if e.key() == Qt.Key_Right and self.active_x < 8:
            self.toggle_activate_tile(self.active_x+1, self.active_y)
        if e.key() == Qt.Key_Left and self.active_x > 0:
            self.toggle_activate_tile(self.active_x-1, self.active_y)            
        if e.key() == Qt.Key_Up and self.active_y > 0:
            self.toggle_activate_tile(self.active_x, self.active_y-1)
        if e.key() == Qt.Key_Down and self.active_y < 8:
            self.toggle_activate_tile(self.active_x, self.active_y+1)
        #Check if the key is a digit and set the number of the active tile
        if e.text().isdigit() and self.tile_active:
            self.set_number(self.active_x, self.active_y, int(e.text()))
        #Backspace clears the number of the active tile
        if e.key() == Qt.Key_Backspace and self.tile_active:
            self.clear_number(self.active_x, self.active_y)
        #Enter deactivates tile
        if e.key() == Qt.Key_Return and self.tile_active:
             self.toggle_activate_tile(self.active_x, self.active_y) 
        if e.key() == Qt.Key_L and self.tile_active:
            self.lock_unlock_number(self.active_x, self.active_y)

    def set_number(self, x, y, n):
        #Set the number in the Sudoku and the tile grid
        self.tile_grid[x][y].set_number(n)
        self.sudoku.sn(x+1, y+1, n)
        if self.sudoku.gs(x+1, y+1) == self.sudoku.WRONG:
            self.tile_grid[x][y].wrong_number = True
        else:
            self.tile_grid[x][y].wrong_number = False       
        #Push to undo stack
        self.undo_stack.append(self.sudoku.copy())
        
        self.update_display()

    def clear_number(self, x, y):
        #Clear the number
        self.tile_grid[x][y].clear_number()
        self.sudoku.sn(x+1, y+1, 0)
        
        #Push to undo stack
        self.undo_stack.append(self.sudoku.copy())        
        
        self.update_display()     

    def lock_unlock_number(self, x, y):
        if self.tile_grid[self.active_x][self.active_y].locked:
            self.tile_grid[self.active_x][self.active_y].unlock()
            self.sudoku.unlock(x+1, y+1)            
        else:
            self.tile_grid[self.active_x][self.active_y].lock()
            self.sudoku.lock(x+1, y+1)
            
        #Push to undo stack
        self.undo_stack.append(self.sudoku.copy())
        
    def set_diagonal_rule(self, state):
        if state == Qt.Checked:
            self.sudoku.diagonal_rule = True
        else:
            self.sudoku.diagonal_rule = False
        self.update_display()               
            
    def iterate_action(self):
        #Iterate the sudoku object
        #print("Starting recursive solve")
        self.sudoku.us()
        
        #Push to undo stack
        self.undo_stack.append(self.sudoku.copy())
        
        self.update_display()
        
    def solve_action(self):
        #Start the recursive solver
        #print("Start solving")
        #Clear old solutions before
        self.solutions.clear()
        #Reset the number of recursive calls      
        self.tries = 1
        #Update the sudoku to set all unambiguous candidates
        self.sudoku.us()
        self.solver_abort = False        
        self.recursive_solver()
        if not self.solver_abort:
            self.status_bar.showMessage("Solver finished after {0} tries".format(self.tries))
        self.next_button.setText("Next solution {0}".format(len(self.solutions)))
        self.next_button.setEnabled(True)            
        #Push to undo stack
        self.undo_stack.append(self.sudoku.copy())
        #Show the first solution if any
        self.next_solution_action()
                
        
    def recursive_solver(self):
        #Solve the sudoku using the recursive backtracking algorithm from:
        #https://www.youtube.com/watch?v=G_UYXzGuqvM
        
        #Abort if max_tries have been exceeded
        if self.tries > self.MAX_TRIES:
            self.status_bar.showMessage("Solver abort after {0} tries".format(self.tries))
            self.solver_abort = True
            return False    

        #Abort if max_tries have been exceeded
        if len(self.solutions) > self.MAX_SOLUTIONS:
            self.status_bar.showMessage("Too many solutions")
            self.solver_abort = True            
            return False                
             

        for r in range(1,10):
            for c in range(1,10):         
                #print("Solve processing r{0}/c{1}".format(r,c))               
                if self.sudoku.gn(r,c) == 0:
                    #print("Still zero r{0}/c{1}".format(r,c))   
                    an = self.sudoku.an(r,c)
                    for n in an:
                        #Try a number from the list of an, but make a backup before
                        backup = self.sudoku.copy()
                        #print("Solver trying {0} for r{1}/c{2}".format(n, r, c))
                        #Count recursive calls
                        self.tries += 1
                        self.sudoku.sn(r,c,n)
                        #Update the sudoku to set all unambiguous candidates
                        self.sudoku.us()
                        #Recursively call solve
                        self.recursive_solver()
                        #Backtracking: Load the backup
                        self.sudoku = backup
                    #print("Solver returning after trying all for r{0}/c{1}".format(r, c))
                    return True#Return after all numbers have been tried
        
        #At this point all possible numbers have been tried for all cell, so the sudoku should be solved
        #print("------------Solver finishing--------------- with {0} tries".format(self.tries))
        #print(self.sudoku)
        #Save the current solution as copy!!!
        self.solutions.append(self.sudoku.copy())
        return True
                                    
                                
                        
    def next_solution_action(self):
        #Cycle display through saved solutions from the recursive solver if any
        if len(self.solutions):
            if self.current_solution < len(self.solutions)-1:
                self.current_solution += 1
            else:
                self.current_solution = 0            
            #Link to the next solutions from the saved solutions
            self.sudoku = self.solutions[self.current_solution]  
            
            self.update_display()
    

    def reset_action(self):
        #Delete all unlocked number
        #and count locked numbers  using as start generation
        start_gen = 0        
        for column in self.tile_grid:
            for tile in column:
                if not tile.locked:# or self.sudoku.gn(tile.x+1, tile.y+1) == 0:
                    self.sudoku.sn(tile.x+1, tile.y+1, 0)
                    self.sudoku.ss(tile.x+1, tile.y+1, self.sudoku.CAND)
                    tile.set_number(0)
                    tile.set_an(self.sudoku.an(tile.x+1, tile.y+1))
                else:
                    start_gen += 1
        self.sudoku.generation = start_gen
                    
        #Push to undo stack
        self.undo_stack.append(self.sudoku.copy())
        
        self.update_display()     



    def update_display(self):
        #Update the gen label
        self.gen_display.setText(str(self.sudoku.generation))        
                
        #Update the displayed numbers and an
        for column in self.tile_grid:
            for tile in column:
                tile.set_number(self.sudoku.gn(tile.x+1, tile.y+1))
                tile.locked = (self.sudoku.gs(tile.x+1, tile.y+1) == self.sudoku.LOCKED)  
                #Find the status 
                self.sudoku.fs(tile.x+1, tile.y+1)
                tile.wrong_number = (self.sudoku.gs(tile.x+1, tile.y+1) == self.sudoku.WRONG)   
                tile.set_an(self.sudoku.an(tile.x+1, tile.y+1))
                #Add the candidate if selected
                if self.candidate_checkbox.isChecked():
                    tile.set_candidate(self.sudoku.gcand(tile.x+1, tile.y+1))
                else:
                    tile.set_candidate(0)
                
                    
    def lock_action(self):
        #Lock all entered numbers
        #and count them using as start generation
        start_gen = 0
        for column in self.tile_grid:
            for tile in column:
                if self.sudoku.gn(tile.x+1, tile.y+1) > 0:
                    self.tile_grid[tile.x][tile.y].lock()
                    self.sudoku.lock(tile.x+1, tile.y+1)
                    start_gen += 1
        self.sudoku.generation = start_gen
        #Push to undo stack
        self.undo_stack.append(self.sudoku.copy())
        self.update_display() 
        
    def undo_action(self):
        #Rewind sudoku object from history
        if self.undo_stack.undo_available():
            self.undo_stack.undo() 
            self.sudoku = self.undo_stack.current_obj().copy()
            self.update_display()  
        
    def redo_action(self):
        #Redo sudoku object from history
        if self.undo_stack.redo_available():               
            self.undo_stack.redo()
            self.sudoku = self.undo_stack.current_obj().copy()
    
            self.update_display()
        

    def load_action(self):
        #Show a file open dialog to get the filename
        file_name = self.show_file_dialog(save = False)
        #If user selected a filename
        if file_name:
            #Open the file and read the json data
            with open(file_name) as f:
                js = json.load(f)
            #Use the from_json factory method to create a new sudoku object
            self.sudoku = json.loads(js, object_hook=Sudoku.from_json)
            
            #Set the diagonal checkbox
            self.diagonal_checkbox.setChecked(self.sudoku.diagonal_rule)
            
            self.next_button.setEnabled(False)  
            #Prepare the list of solutions for the recursive solver
            self.solutions = []
            self.current_solution = 0             
            
            #Prepare the Undo/Redo Stack
            self.undo_stack = Undo_Redo()
            #Push to undo stack
            self.undo_stack.append(self.sudoku.copy())   
            
            #Set the title
            self.setWindowTitle("Sudoku Solver – " + os.path.basename(file_name))
                
            self.update_display()
                                                    
            
    def new_action(self):
        #Reset to empty sudoku
        #Use the from_json factory method to create a new sudoku object
        #Prepare the numeric sudoku object
        self.sudoku = Sudoku()
        
        #Prepare the Undo/Redo Stack
        self.undo_stack = Undo_Redo()
        #Push to undo sta
        self.undo_stack.append(self.sudoku.copy())        
        
        #The active tile in the grid
        self.active_x = 0
        self.active_y = 0
        #True if a tile is activated
        self.tile_active = False;     
        
        #Prepare the list of solutions for the recursive solver
        self.solutions = []
        self.current_solution = 0 
        self.next_button.setEnabled(False)  
        #Set the title
        self.setWindowTitle("Sudoku Solver")              
        self.update_display()      

    def save_action(self):
        #Show a file save dialog to get the filename
        file_name = self.show_file_dialog(save = True)
        #If user selected a filename
        if file_name:
            #Open the file and write the json representation of the current sudoku object
            with open(file_name, "w") as f:
                json.dump(self.sudoku.to_json(), f)
            #Set the title
            self.setWindowTitle("Sudoku Solver – " + os.path.basename(file_name))                
            


    def show_file_dialog(self, save = False):
        """ Show native file dialog for open or save of a dat file
            Presents the last used folder retrieved from the preferences
        ### Returns:
            {str}: file path            
        """
        #Present file dialog using last saved folder

        dialog = QFileDialog(self)
        lastFolder = self.getLastSaveFolder()        
        dialog.setDirectory(lastFolder)        
        dialog.setWindowTitle("Save Sudoku grid")
        dialog.setNameFilters(["Dat files (*.dat)", "Any Files (*)"])
        dialog.setDefaultSuffix("dat")
        if save: 
            dialog.setFileMode(QFileDialog.AnyFile) #Select also non-existing files
            dialog.setAcceptMode(QFileDialog.AcceptSave)        
        else:
            dialog.setFileMode(QFileDialog.ExistingFile) #Select existing file
            dialog.setAcceptMode(QFileDialog.AcceptOpen)            

        #Fallback to Qt save dialog if MacOS native dialog crashes
        #dialog.setOptions(QFileDialog.DontUseNativeDialog)
        if dialog.exec_() == QDialog.Accepted:
            file_name = dialog.selectedFiles()[0]            
            #Save selected foldername for next time
            self.saveLastFolder(file_name)
            return file_name
        else:
            return None        
    


    def getLastSaveFolder(self):
        """ Try to get a selected folder from QSettings file
            (Mac: ~\library\preferences\)
            Defaults to userfolder ~
        ### Returns:
            {str}: folder path
        """
        try:
            settings = QtCore.QSettings('sudokuSolver', 'sudokuSolver')
            lastFolder = settings.value('saveFolder', type=str)
            
        except:
            lastFolder = os.path.expanduser('~')

        return lastFolder


    def saveLastFolder(self, foldername):
        """ Saves the last visited folder as QSettings
            (Mac: ~\library\preferences\)
        ### Args:
            foldername {str}: foldername
        """
        settings = QtCore.QSettings('sudokuSolver', 'sudokuSolver')
        settings.setValue('saveFolder', os.path.dirname(foldername))


    def textchanged(self, text):
        """_summary_
            修改输入框数值之后会发生的变化
        Args:
            text (_type_): _description_
        """
        # print(text)
        for i in range(len(text)):
            if text[i] != '0':
                self.set_number( i % 9, i // 9, int(text[i]))
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()



# Easy: "085000210094012003000300704503409000040206030000103907608005000100840360027000890"