#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################
# File Name  : sudoku_solver
# Author     : liyanqing
# Created On : 2020-12-10 04:01:42
################################
import os
import re
import sys
import copy

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QTextEdit, QTabWidget, QFrame, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QMessageBox, QHeaderView, QDesktopWidget, QFileDialog
from PyQt5.QtGui import QBrush, QFont, QTextCursor, QColor
from PyQt5.QtCore import Qt

os.environ['PYTHONUNBUFFERED']='1'

def set_window_center(window):
    """
    Move the input GUI window into the center of the computer windows.
    """
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())

def set_text_position(textEditItem, position='End'):
    """
    For QTextEdit widget, show the 'Start' or 'End' part of the text.
    """
    cursor = textEditItem.textCursor()

    if position == 'Start':
        cursor.movePosition(QTextCursor.Start)
    elif position == 'End':
        cursor.movePosition(QTextCursor.End)

    textEditItem.setTextCursor(cursor)
    textEditItem.ensureCursorVisible()


class mainWindow(QMainWindow):
    """
    Main window of sudoku_solver.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.step_list = []
        self.current_step = -1

    #############
    #### GUI ####
    #############
    def init_ui(self):
        """
        Main process, draw the main graphic frame.
        """
        # Add menu bar.
        self.gen_menu_bar()

        # Add main_tab.
        self.gen_main_tab()

        # Draw GUI.
        self.setWindowTitle('Sudoku Solver')
        self.resize(1010, 700)
        set_window_center(self)

    def gen_menu_bar(self):
        """
        Generate menu bar.
        """
        menu_bar = self.menuBar()

        # File
        save_action = QAction('保存', self)
        save_action.triggered.connect(self.save_data)

        load_action = QAction('载入', self)
        load_action.triggered.connect(self.load_data)

        exit_action = QAction('退出', self)
        exit_action.triggered.connect(qApp.quit)

        file_menu = menu_bar.addMenu('文件')
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addAction(exit_action)

        # Setup
        generate_easy_test_data_action = QAction('生成测试数据(容易)', self)
        generate_easy_test_data_action.triggered.connect(lambda:self.generate_test_data('easy'))

        generate_middle_test_data_action = QAction('生成测试数据(中间)', self)
        generate_middle_test_data_action.triggered.connect(lambda:self.generate_test_data('middle'))

        generate_advanced_test_data_action = QAction('生成测试数据(高级)', self)
        generate_advanced_test_data_action.triggered.connect(lambda:self.generate_test_data('advanced'))

        generate_advanced_plus_test_data_action = QAction('生成测试数据(高级+)', self)
        generate_advanced_plus_test_data_action.triggered.connect(lambda:self.generate_test_data('advanced_plus'))

        generate_super_test_data_action = QAction('生成测试数据(变态)', self)
        generate_super_test_data_action.triggered.connect(lambda:self.generate_test_data('super'))

        clear_action = QAction('清空', self)
        clear_action.triggered.connect(self.clear_data)

        setup_menu = menu_bar.addMenu('设置')
        setup_menu.addAction(generate_easy_test_data_action)
        setup_menu.addAction(generate_middle_test_data_action)
        setup_menu.addAction(generate_advanced_test_data_action)
        setup_menu.addAction(generate_advanced_plus_test_data_action)
        setup_menu.addAction(generate_super_test_data_action)
        setup_menu.addAction(clear_action)

        # Help
        about_action = QAction('关于 Sudoku Solver', self)
        about_action.triggered.connect(self.show_about)

        help_menu = menu_bar.addMenu('帮助')
        help_menu.addAction(about_action)

    def save_data(self):
        """
        Save self.sudoku_table data into a file.
        """
        # Check the original data valid or not.
        if self.check_sudoku_table_data_validation():
            (sudoku_file, fileType) = QFileDialog.getSaveFileName(self, 'Save sudoku data', '.', 'Text Files (*.txt)')

            if sudoku_file:
                self.get_sudoku_table_data()

                with open(sudoku_file, 'w') as SF:
                    for (row, column_list) in enumerate(self.sudoku_data_dic['row']):
                        row_string = ''

                        for (column, cell_value) in enumerate(column_list):
                            if cell_value:
                                row_string = str(row_string) + str(cell_value)
                            else:
                                row_string = str(row_string) + ' '

                        SF.write(str(row_string) + '\n')

    def load_data(self):
        """
        Update self.sudoku_table with the data from a file
        """
        self.clear_data()
        (sudoku_file, fileType) = QFileDialog.getOpenFileName(self, 'Load sudoku data', '.', 'Text Files (*.txt)')

        if sudoku_file:
            row_list = []

            with open(sudoku_file, 'r') as SF:
                for line in SF.readlines():
                    line = re.sub('\n', '', line)
                    line_list = list(line)

                    if len(line_list) == 9:
                        row_list.append(line_list)
                    else:
                        error_message = """*错误*：输入的sudoku文件如下行格式错误，必须有9个字符位（含空格）。
""" + str(line)
                        QMessageBox.critical(self, 'Sudoku Solver', error_message)

            if len(row_list) == 9:
                self.update_sudoku_table(row_list)
            else:
                error_message = '*错误*：输入的sudoku文件格式错误，必须有9行字符。'
                QMessageBox.critical(self, 'Sudoku Solver', error_message)

    def generate_test_data(self, mode):
        """
        Fill demo sukodu data into self.sukodu_table.
        """
        self.clear_data()

        test_list_dic = {
                         'easy' : [
                                   ['2', '7', ' ', ' ', ' ', '8', ' ', '5', ' '],
                                   [' ', ' ', '1', ' ', ' ', '3', '8', ' ', ' '],
                                   ['5', ' ', ' ', '2', ' ', ' ', ' ', ' ', '1'],
                                   ['6', '1', ' ', ' ', ' ', ' ', ' ', '8', ' '],
                                   [' ', '4', '2', ' ', ' ', ' ', '9', ' ', ' '],
                                   [' ', ' ', ' ', '1', '6', '9', ' ', ' ', '7'],
                                   [' ', '2', ' ', ' ', '4', ' ', '1', ' ', '5'],
                                   [' ', '9', '3', ' ', '8', ' ', ' ', '6', ' '],
                                   ['1', ' ', '7', '9', ' ', ' ', ' ', '3', ' '],
                                  ],
                         'middle' : [
                                     [' ', '7', ' ', ' ', '4', ' ', ' ', '9', ' '],
                                     [' ', ' ', '9', ' ', '7', ' ', '8', ' ', ' '],
                                     ['5', ' ', ' ', ' ', ' ', '9', ' ', ' ', '7'],
                                     [' ', '3', ' ', ' ', ' ', '1', '2', ' ', '8'],
                                     ['8', ' ', ' ', ' ', '9', ' ', '6', ' ', ' '],
                                     [' ', '6', '7', '5', ' ', '8', ' ', ' ', ' '],
                                     ['3', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' '],
                                     [' ', ' ', ' ', '9', ' ', ' ', ' ', '8', '5'],
                                     ['6', ' ', '8', '3', ' ', ' ', ' ', '2', '9'],
                                    ],
                         'advanced' : [
                                       ['8', ' ', ' ', ' ', ' ', ' ', '1', '5', ' '],
                                       [' ', '9', ' ', '3', ' ', ' ', '2', ' ', ' '],
                                       [' ', '4', ' ', '6', '5', ' ', ' ', ' ', ' '],
                                       [' ', ' ', '2', ' ', ' ', ' ', '8', '1', ' '],
                                       [' ', ' ', ' ', '4', ' ', ' ', ' ', ' ', '2'],
                                       [' ', '1', ' ', ' ', '8', '7', ' ', ' ', '5'],
                                       ['7', ' ', ' ', ' ', ' ', '6', ' ', ' ', ' '],
                                       [' ', ' ', '4', ' ', '3', ' ', ' ', '6', '1'],
                                       [' ', ' ', '5', ' ', ' ', '2', '3', ' ', ' '],
                                      ],
                         'advanced_plus' : [
                                            [' ', '7', ' ', ' ', ' ', ' ', ' ', '1', ' '],
                                            [' ', ' ', ' ', '8', '1', '4', ' ', ' ', ' '],
                                            ['8', ' ', ' ', ' ', ' ', ' ', '2', ' ', '9'],
                                            ['5', '9', ' ', ' ', '3', ' ', ' ', ' ', ' '],
                                            [' ', ' ', ' ', ' ', ' ', '6', ' ', '5', ' '],
                                            [' ', '6', ' ', '9', ' ', ' ', ' ', ' ', '7'],
                                            [' ', ' ', ' ', '6', ' ', '8', ' ', ' ', ' '],
                                            ['4', ' ', ' ', ' ', ' ', '5', ' ', ' ', '8'],
                                            ['2', ' ', ' ', ' ', ' ', ' ', '3', '9', ' '],
                                           ],
                         'super' : [
                                    ['2', ' ', ' ', ' ', '6', ' ', ' ', ' ', '5'],
                                    ['5', ' ', ' ', '4', ' ', ' ', ' ', ' ', ' '],
                                    [' ', '6', ' ', ' ', ' ', ' ', '3', '4', ' '],
                                    [' ', '2', ' ', ' ', ' ', ' ', ' ', '9', ' '],
                                    [' ', ' ', '3', '1', '5', '8', ' ', ' ', '7'],
                                    ['1', ' ', ' ', '6', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', '8', '3', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', '1', ' ', '5', ' ', ' '],
                                    [' ', '5', ' ', ' ', ' ', ' ', '9', '6', ' '],
                                   ],
                        }

        test_list = test_list_dic[mode]

        for row in range(9):
            for column in range(9):
                test_data = test_list[row][column]

                if test_data != ' ':
                    self.sudoku_table.item(row, column).setText(test_data)
                    self.sudoku_table.item(row, column).setFont(QFont('Times', 24, QFont.Black))

    def clear_data(self):
        self.gen_sudoku_table()
        self.step_text.setText('')
        self.step_list = []
        self.current_step = -1

    def show_about(self):
        """
        Show sudoku solver about information.
        """
        about_message = """
      数独是一种数字智力拼图游戏，起源于18世纪末的瑞士，后在美国发展，在日本得以发扬光大。
      数独盘面是个九宫，每一宫又分为九个小格。在这八十一格中给出一定的已知数字和解题条件，利用逻辑和推理，在其他的空格上填入1-9的数字。使1-9每个数字在每一行、每一列和每一宫中都只出现一次，所以又称“九宫格”。
      如下是数独的一些基本概念：
* 单元格 (cell) ：数独盘面上的最小格点，用于填充数字，共有9x9=81个单元格。
* 行（row）：数独盘面上的一行数据，一共有9行。
* 列（column）：数独盘面上的一列数据，一共有9列。
* 块（block）：也叫宫，或者色块（每块涂有不同颜色），包含9个单元格。数独盘面上一共有9个块，编号1-9，排布如下：
                        1 2 3
                        4 5 6
                        7 8 9

      数独的解法分为“直观法”和“候选数法”两大类，又细分为多种不同的解题方法。
* 直观法
   唯一解法
   基础摒除法
   区块摒除法
   唯余解法
   矩形摒除法
   单元摒除法
   余数测试法
* 候选数法
   唯一候选数法
   隐性唯一候选数法
   三链数删减法
   隐性三链数删减法
   矩形顶点删减法
   三链列删减法
   关键数删减法

      本工具 Sudoku Solver是一个专为数独设计的解题器，主要采用如上的候选数法（唯一候选数法，关键数删减法）和直观法（区块摒除法），可以解决绝大部分的数独题目。
      Sudoku Solver支持一步式解题及分布式解题，不但可以帮助用户得到数独解题结果，还可以帮助用户了解数独的解题思路。
      如下是Sudoku Solver的一些基本概念：
1. Sudoku Solver提供一个空白界面，用户需要自己填入初始的数据。（也可从“设置”菜单栏中载入测试数据）
2. Sudoku Solver解题过程中，黑色大字是初始填入的数独数据，黑色小字是解题过程中单元格上可能的数字，绿色大字是最后计算出来的解。

      如果用户遇到任何Sudoku Solver无法解决的数独题目，请将题目发送至如下作者邮箱（最好提供截图），作者会尽快优化工具。

作者：李艳青
联系方式：liyanqing1987@163.com
"""
        QMessageBox.about(self, '关于Sudoku Solver', about_message)

    def gen_main_tab(self):
        """
        Generate main tab.
        """
        self.main_tab = QTabWidget(self)
        self.setCentralWidget(self.main_tab)

        self.sudoku_frame = QFrame(self.main_tab)
        self.sudoku_frame.setFrameShadow(QFrame.Raised)
        self.sudoku_frame.setFrameShape(QFrame.Box)

        self.step_frame = QFrame(self.main_tab)
        self.step_frame.setFrameShadow(QFrame.Raised)
        self.step_frame.setFrameShape(QFrame.Box)

        self.description_frame = QFrame(self.main_tab)
        self.description_frame.setFrameShadow(QFrame.Raised)
        self.description_frame.setFrameShape(QFrame.Box)

        # Layout
        main_tab_grid = QGridLayout()

        main_tab_grid.addWidget(self.sudoku_frame, 0, 0)
        main_tab_grid.addWidget(self.step_frame, 0, 1)
        main_tab_grid.addWidget(self.description_frame, 1, 0, 1, 2)

        main_tab_grid.setRowStretch(0, 6)
        main_tab_grid.setRowStretch(1, 1)
        main_tab_grid.setColumnStretch(0, 10)
        main_tab_grid.setColumnStretch(1, 9)

        self.main_tab.setLayout(main_tab_grid)

        # Generate sub frames.
        self.gen_sudoku_frame()
        self.gen_step_frame()
        self.gen_description_frame()

    def gen_sudoku_frame(self):
        """
        Generate self.main_tab -> self.sudoku_frame.
        """
        self.sudoku_title_label = QLabel(self.sudoku_frame)
        self.sudoku_title_label.setText('数独')
        self.sudoku_title_label.setAlignment(Qt.AlignCenter)
        self.sudoku_table = QTableWidget(self.sudoku_frame)

        # Layout
        sudoku_frame_grid = QGridLayout()
        sudoku_frame_grid.addWidget(self.sudoku_title_label, 0, 0)
        sudoku_frame_grid.addWidget(self.sudoku_table, 1, 0)
        self.sudoku_frame.setLayout(sudoku_frame_grid)

        sudoku_frame_grid.setRowStretch(0, 1)
        sudoku_frame_grid.setRowStretch(1, 18)

        # Generate sub table.
        self.gen_sudoku_table()

    def gen_sudoku_table(self):
        """
        Generate self.main_tab -> self.sudoku_frame -> self.sudoku_table.
        """
        self.sudoku_table.setShowGrid(True)
        self.sudoku_table.setRowCount(9)
        self.sudoku_table.setColumnCount(9)

        self.sudoku_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sudoku_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.sudoku_table.setVerticalHeaderLabels([str(i) for i in range(1,10)])
        self.sudoku_table.setHorizontalHeaderLabels([str(i) for i in range(1,10)])

        # Set background color.
        for row in range(9):
            for column in range(9):
                item = QTableWidgetItem(' ')
                self.sudoku_table.setItem(row, column, item)
                self.sudoku_table.item(row, column).setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)

                if (((0 <= row <= 2) or (6 <= row <= 8)) and (3 <= column <= 5)) or ((3 <= row <= 5) and ((0 <= column <= 2) or (6 <= column <= 8))):
                    self.sudoku_table.item(row, column).setBackground(QColor(225, 255, 255))

    def gen_step_frame(self):
        """
        Generate self.main_tab -> self.step_frame.
        """
        all_step_button = QPushButton('一键解题', self.step_frame)
        all_step_button.clicked.connect(self.all_steps)

        previous_step_button = QPushButton('上一步', self.step_frame)
        previous_step_button.clicked.connect(self.previous_step)

        next_step_button = QPushButton('下一步', self.step_frame)
        next_step_button.clicked.connect(self.next_step)

        self.step_text = QTextEdit(self.step_frame)

        # Layout
        step_frame_grid = QGridLayout()

        step_frame_grid.addWidget(all_step_button, 0, 0, 1, 2)
        step_frame_grid.addWidget(previous_step_button, 1, 0)
        step_frame_grid.addWidget(next_step_button, 1, 1)
        step_frame_grid.addWidget(self.step_text, 2, 0, 1, 2)

        self.step_frame.setLayout(step_frame_grid)

    def gen_description_frame(self):
        """
        Generate self.main_tab -> self.description_frame.
        """
        description_text = QTextEdit(self.description_frame)
        description_string = """* 数独规则：
   数独有9x9个单元格，部分单元格中已经填好数字，填补其它空白单元格，使每一行/每一列/每个色块都包含1-9这9个数字且不重复。
* Sudoku Solver用法：
   手工填入数独初始值（可以从https://www.sudoku-cn.com获取），点击“一键解题”或“上一步/下一步”来一次性或者分步获取数独结果。"""
        description_text.insertPlainText(description_string)
        description_text.setFocusPolicy(Qt.NoFocus)

        # Layout
        description_frame_grid = QGridLayout()
        description_frame_grid.addWidget(description_text, 0, 0)
        self.description_frame.setLayout(description_frame_grid)

    ##################
    #### Function ####
    ##################
    def all_steps(self):
        """
        Show all steps.
        """
        if not self.step_list:
            self.solve_sudoku()

        self.show_step()
        self.current_step = len(self.step_list)-1

    def previous_step(self):
        """
        Show previous step.
        """
        if not self.step_list:
            self.solve_sudoku()

        if 1 <= self.current_step < len(self.step_list):
            self.current_step -= 1
            self.show_step()

    def next_step(self):
        """
        Show next step.
        """
        if not self.step_list:
            self.solve_sudoku()

        if -1 <= self.current_step < len(self.step_list)-1:
            self.current_step += 1
            self.show_step()

    ## Solve Sudoku (start) ##
    def solve_sudoku(self):
        """
        Solve the sudoku.
        1. fill_cell_possible_numbers (Fill empty cells with possible numbers). 
           If meet error, show error message and exit, else, continue.
        2. Try to solve sudoku with unique_candidate_number_method and block_exclusion_method.
           If sudoku is solved, show pass message and exit, else, continue.
        3. Try to solve sudoku with key_number_reduction_method (unique_candidate_number_method and block_exclusion_method will also be repeated).
           If sudoku is solved, show pass message and exit, else, show suggestion and exit.
        """
        # Check the original data valid or not.
        if self.check_sudoku_table_data_validation():
            self.update_step_list(['#############', '#  空白单元格初始化  #', '#############'])
            self.update_step_list(['', '> 在空白单元格中填充所有可能的数字。'])

            # Fill empty cells with possible numbers.
            if not self.fill_cell_possible_numbers():
                # If meet error on self.fill_cell_possible_numbers. return.
                return(False)
            else:
                if self.check_sudoku_result():
                    # If sudoku is solved, return.
                    return(True)
                else:
                    # If sudoku is not solved, try to solve sudoku with unique_candidate_number_method and block_exclusion_method in loop.
                    if self.solve_sudoku_with_basic_methods():
                        # If sudoku is solved, return.
                        return(True)
                    else:
                        # If unique_candidate_number_method and block_exclusion_method cannot solve the sudoku, try key_number_reduction_method.
                        if self.key_number_reduction_method():
                            # If sudoku is solved, return.
                            return(True)
                        else:
                            # If sudoku is not solved, return.
                            self.update_step_list(['', '抱歉，解题失败！', '请联系liyanqing1987@163.com并提供数独截图，作者会尽快解决。'], ['抱歉，解题失败！', '请联系liyanqing1987@163.com并提供数独截图，作者会尽快解决。',])

    def check_sudoku_table_data_validation(self):
        """
        Check self.sudoku_table data valid or not.
        """
        find_valid_data = False

        for row in range(9):
            for column in range(9):
                cell_value = self.sudoku_table.item(row, column).text().strip()

                if re.match('^\s*$', cell_value):
                    pass
                elif re.match('^[1-9]$', cell_value):
                    find_valid_data = True
                else:
                    error_message = '*错误*: 第' + str(row+1) + '行第' + str(column+1) + '列单元格的值"' + str(cell_value) + '"非法, 必须是空行，或者1-9之间的数字。'
                    QMessageBox.critical(self, 'Sudoku Solver', error_message)
                    return(False)

        if not find_valid_data:
            error_message = '*错误*：不能保存空的sudoku数据。'
            QMessageBox.critical(self, 'Sudoku Solver', error_message)
            return(False)

        # For every row/column/block, 1-9 can only appear once.
        self.get_sudoku_table_data()

        for (row, row_list) in enumerate(self.sudoku_data_dic['row']):
            for (column, cell_value) in enumerate(row_list):
                if cell_value and (cell_value in row_list[0:column]):
                    error_message = '*错误*: 第' + str(row+1) + '行第' + str(column+1) + '列单元格的值"' + str(cell_value) + '"在第' + str(row+1) + '行重复出现。'
                    QMessageBox.critical(self, 'Sudoku Solver', error_message)
                    return(False)

        for (column, column_list) in enumerate(self.sudoku_data_dic['column']):
            for (row, cell_value) in enumerate(column_list):
                if cell_value and (cell_value in column_list[0:row]):
                    error_message = '*错误*: 第' + str(row+1) + '行第' + str(column+1) + '列单元格的值"' + str(cell_value) + '"在第' + str(column+1) + '列重复出现。'
                    QMessageBox.critical(self, 'Sudoku Solver', error_message)
                    return(False)

        for (block_num, block_list) in enumerate(self.sudoku_data_dic['block']):
            for (i, cell_value) in enumerate(block_list):
                row = (block_num//3)*3 + i//3
                column = (block_num%3)*3 + i%3

                if cell_value and (cell_value in block_list[0:i]):
                    error_message = '*错误*: 第' + str(row+1) + '行第' + str(column+1) + '列单元格的值"' + str(cell_value) + '"在第' + str(block_num+1) + '色块重复出现。'
                    QMessageBox.critical(self, 'Sudoku Solver', error_message)
                    return(False)

        return(True)

    def get_sudoku_table_data(self):
        """
        Parse self.sudoku_table and get all cell values.
        """
        self.sudoku_data_dic = {
                                'row' : [['' for i in range(9)] for j in range(9)],
                                'column' : [['' for i in range(9)] for j in range(9)],
                                'block' : [[] for j in range(9)],
                               }

        for row in range(9):
            for column in range(9):
                cell_value = self.sudoku_table.item(row, column).text().strip()

                self.sudoku_data_dic['row'][row][column] = cell_value
                self.sudoku_data_dic['column'][column][row] = cell_value
                block_num = (row//3)*3 + column//3
                self.sudoku_data_dic['block'][block_num].append(cell_value)

    def update_step_list(self, step_text_list=[], message_text_list=[]):
        """
        Save current 'row_list'/'step_text'/'message_text' information into self.step_list.
        """
        self.get_sudoku_table_data()

        step_dic = {
                    'row_list' : copy.deepcopy(self.sudoku_data_dic['row']),
                    'step_text' : copy.deepcopy(step_text_list),
                    'message_text' : copy.deepcopy(message_text_list),
                   }

        self.step_list.append(step_dic)

    def fill_cell_possible_numbers(self, specified_row=-1, specified_column=-1, specified_block_num=-1):
        """
        For every cell, get all possible numbers (not on the same row/column/block) and fill in.
        """
        for row in range(9):
            if (specified_row == -1) or (specified_row == row):
                for column in range(9):
                    if (specified_column == -1) or (specified_column == column):
                        cell_value = self.sudoku_table.item(row, column).text().strip()

                        # Only fill the cell whose value is not a single number.
                        if not re.match('^[1-9]$', cell_value):
                            block_num = (row//3)*3 + column//3

                            if (specified_block_num == -1) or (specified_block_num == block_num):
                                possible_number_list = []
                                cell_value_list = list(cell_value)

                                for number in range(1,10):
                                    number = str(number)

                                    # If a number is not on the same row/column/block, them append it into the possible number list.
                                    if (number not in self.sudoku_data_dic['row'][row]) and (number not in self.sudoku_data_dic['column'][column]) and (number not in self.sudoku_data_dic['block'][block_num]):
                                        if (not cell_value_list) or (number in cell_value_list):
                                            possible_number_list.append(number)

                                # If not find any possible number, show error message.
                                if not possible_number_list:
                                    self.update_step_list(['', '    *错误*: 第' + str(row+1) + '行第' + str(column+1) + '列单元格没有发现可行的数字，原始的数独数据应该是不合法的。'], ['*错误*: 第' + str(row+1) + '行第' + str(column+1) + '列单元格没有发现可行的数字，原始的数独数据应该是不合法的。',])
                                    return(False)
                                else:
                                    possible_number_string = ''.join(possible_number_list)

                                    if possible_number_string != cell_value:
                                        if cell_value_list:
                                            if (specified_row != -1) or (specified_column != -1) or (specified_block_num != -1):
                                                self.update_step_list(['        第' + str(row+1) + '行第' + str(column+1) + '列单元格可行的数字更新为 "' + str(possible_number_string) + '"。  (' + str(cell_value) + ' -> ' + str(possible_number_string) + ')',])
                                            else:
                                                self.update_step_list(['    第' + str(row+1) + '行第' + str(column+1) + '列单元格可行的数字更新为 "' + str(possible_number_string) + '"。  (' + str(cell_value) + ' -> ' + str(possible_number_string) + ')',])
                                        else:
                                            self.update_step_list(['    第' + str(row+1) + '行第' + str(column+1) + '列单元格发现可行的数字 "' + str(possible_number_string) + '"。',])

                                        self.sudoku_table.item(row, column).setText(possible_number_string)
                                        self.update_step_list()

                                        # For some cell, once the possible number is limited to only one, then re-count possible numbers for the cells on the same row/column/block.
                                        if len(possible_number_list) == 1:
                                            if (not self.fill_cell_possible_numbers(specified_row=row)) or (not self.fill_cell_possible_numbers(specified_column=column)) or (not self.fill_cell_possible_numbers(specified_block_num=block_num)):
                                                return(False)

        return(True)

    def check_sudoku_result(self):
        """
        Check self.sudoku_table data result.
        """
        # Make sure cell data type is vaild.
        for row in range(9):
            for column in range(9):
                cell_value = self.sudoku_table.item(row, column).text().strip()

                if not re.match('^[1-9]$', cell_value):
                    return(False)

        # Make sure row data contains 1-9.
        self.get_sudoku_table_data()

        for row in range(9):
            row_list = [int(i) for i in self.sudoku_data_dic['row'][row]]

            if sorted(row_list) != list(range(1, 10)):
                return(False)

        # Make sure column data contains 1-9.
        for column in range(9):
            column_list = [int(i) for i in self.sudoku_data_dic['column'][column]]

            if sorted(column_list) != list(range(1, 10)):
                return(False)

        self.update_step_list(['', '解题成功!'], ['解题成功!',])

        return(True)

    def solve_sudoku_with_basic_methods(self):
        """
        Try to solve sudoku with unique_candidate_number_method and block_exclusion_method in loop.
        """
        while True:
            # Save the initial self.sudoku_table data.
            self.get_sudoku_table_data()
            row_data_dic = self.sudoku_data_dic['row']

            # Save the init data.
            if not self.unique_candidate_number_method():
                # If self.unique_candidate_number_method meet error, return False.
                return(False)
            else:
                if self.check_sudoku_result():
                    # If sudoku is solved, return True.
                    return(True)
                else:
                    # If sudoku is not solved, try block_exclusion_method.
                    if not self.block_exclusion_method():
                        # If self.block_exclusion_method meet error, return False.
                        return(False)
                    else:
                        if self.check_sudoku_result():
                            # If sudoku is solved, return True.
                            return(True)
                        else:
                            # If sudoku is not solved, and no update on the self.sudoku_table afte the two methods, exit the endless loop.
                            self.get_sudoku_table_data()

                            if row_data_dic == self.sudoku_data_dic['row']:
                                return(False)

    def unique_candidate_number_method(self):
        """
        唯一候选数法。
        唯一候选数法解题的过程就是逐渐排除不合适的候选数的过程，当某个宫格的候选数排除到只有一个数的时候，那么这个数就是该宫格的唯一的一个候选数，这个候选数就是解了。
        """
        self.update_step_list(['', '', '##########', '# 唯一候选数法 #', '##########'])

        time = 0

        while True:
            # Save the original self.sudoku_table data.
            self.get_sudoku_table_data()
            row_data_dic = self.sudoku_data_dic['row']

            # Find unique number on every color block.
            time += 1
            self.update_step_list(['', '> 找到每个色块中仅出现一次的数字。  (第' + str(time) + '次)'])

            if not self.find_unique_number():
                return(False)
            else:
                # If no update on the self.sudoku_table, exit the endless loop.
                self.get_sudoku_table_data()

                if row_data_dic == self.sudoku_data_dic['row']:
                    break

        return(True)

    def find_unique_number(self):
        """
        If a number in the color block only appears once, then the cell where the number is located can determine the unique value.
        """
        for row in range(9):
            for column in range(9):
                cell_value = self.sudoku_table.item(row, column).text()
                cell_value_list = list(cell_value)

                # Only check the cell who have more than one number.
                if len(cell_value_list) > 1:
                    block_num = (row//3)*3 + column//3
                    block_number_strings = ''

                    for block_number_string in self.sudoku_data_dic['block'][block_num]:
                        block_number_strings = str(block_number_strings) + str(block_number_string)

                    for number in cell_value_list:
                        if block_number_strings.count(number) == 1:    
                            self.update_step_list(['    色块' + str(block_num+1) + ', 第' + str(row+1) + '行第' + str(column+1) + '列单元格发现色块中的唯一值 "' + str(number) + '"。  (' + str(cell_value) + ' -> ' + str(number) + ')'])
                            self.sudoku_table.item(row, column).setText(number)
                            self.update_step_list()

                            # For some cell, once the possible number is limited to only one, then re-count possible numbers for the cells on the same row/column/block.
                            if (not self.fill_cell_possible_numbers(specified_row=row)) or (not self.fill_cell_possible_numbers(specified_column=column)) or (not self.fill_cell_possible_numbers(specified_block_num=block_num)):
                                return(False)

                            break

        return(True)

    def block_exclusion_method(self):
        """
        区块摒除法。
        在色块中，如果某一数值仅出现在某行或某列中，那么这一行或者这一列中其它色块的数据都可以排除掉这个数值。
        """
        self.update_step_list(['', '', '#########', '# 区块摒除法 #', '#########'])
        self.get_sudoku_table_data()

        for block_num in range(9):
            if not self.parse_block_num_with_exclusion(block_num, self.sudoku_data_dic['block'][block_num]):
                return(False)

        return(True)

    def parse_block_num_with_exclusion(self, block_num, block_list):
        """
        parse the block data and get the exclusive row/column.
        """
        self.update_step_list(['', '> 找到色块' + str(block_num+1) + '中只出现在某行或者某列的数字。'])

        exclusive_dic = {}

        # Check cells who have more than one number.
        for i in range(9):
            number_list = list(block_list[i])

            if len(number_list) > 1:
                row = (block_num//3)*3 + i//3
                column = (block_num%3)*3 + i%3

                for number in number_list:
                    if number in exclusive_dic.keys():
                        if row not in exclusive_dic[number]['row']:
                            exclusive_dic[number]['row'].append(row)

                        if column not in exclusive_dic[number]['column']:
                            exclusive_dic[number]['column'].append(column)
                    else:
                        exclusive_dic.setdefault(number, {'row' : [row,], 'column' : [column,]})

        # Find the only number on the block.
        for number in exclusive_dic.keys():
            if len(exclusive_dic[number]['row']) == 1:
                row = exclusive_dic[number]['row'][0]
                self.update_step_list(['    色块' + str(block_num+1) + ', 值 "' + str(number) + '" 仅出现在第' + str(row+1) + '行中。',])

                block_column_list = [(block_num%3)*3, (block_num%3)*3+1, (block_num%3)*3+2]

                for column in range(9):
                    row_string = self.sudoku_table.item(row, column).text().strip()

                    if column not in block_column_list:
                        if re.search(str(number), row_string):
                            self.update_step_list(['    第' + str(row+1) + '行第' + str(column+1) + '列, 从可行数字列表中移除数字 "' + str(number) + '"。',])
                            row_string = re.sub(str(number), '', row_string)
                            self.sudoku_table.item(row, column).setText(row_string)
                            self.update_step_list()

                            if len(list(row_string)) == 1:
                                if (not self.fill_cell_possible_numbers(specified_row=row)) or (not self.fill_cell_possible_numbers(specified_column=column)) or (not self.fill_cell_possible_numbers(specified_block_num=block_num)):
                                    return(False)
            elif len(exclusive_dic[number]['column']) == 1:
                column = exclusive_dic[number]['column'][0]
                self.update_step_list(['    色块' + str(block_num+1) + ', 值 "' + str(number) + '" 仅出现在第' + str(column+1) + '列中。',])

                block_row_list = [(block_num//3)*3, (block_num//3)*3+1, (block_num//3)*3+2]

                for row in range(9):
                    column_string = self.sudoku_table.item(row, column).text().strip()

                    if row not in block_row_list:
                        if re.search(str(number), column_string):
                            self.update_step_list(['    第' + str(row+1) + '行第' + str(column+1) + '列, 从可行数字列表中移除数字 "' + str(number) + '"。',])
                            column_string = re.sub(str(number), '', column_string)
                            self.sudoku_table.item(row, column).setText(column_string)
                            self.update_step_list()

                            if len(list(column_string)) == 1:
                                if (not self.fill_cell_possible_numbers(specified_row=row)) or (not self.fill_cell_possible_numbers(specified_column=column)) or (not self.fill_cell_possible_numbers(specified_block_num=block_num)):
                                    return(False)

        return(True)

    def key_number_reduction_method(self):
        """
        关键数删减法。
        关键数删减法就是在后期找到一个数，这个数在行（或列，九宫格）仅出现两次的数字。我们假定这个数在其中一个宫格类，继续求解，如果发生错误，则确定我们的假设错误。如果继续求解仍然出现困难，不妨假设这个数在另外一个宫格，看能不能得到错误。这就是关键数删减法。
        """
        self.update_step_list(['', '', '##########', '# 关键数删减法 #', '##########'])

        last_step_list = copy.deepcopy(self.step_list)
        last_row_list = copy.deepcopy(self.step_list[-1]['row_list'])

        for (row, row_list) in enumerate(self.sudoku_data_dic['row']):
            for (column, cell_value) in enumerate(row_list):
                if len(list(cell_value)) > 1:
                    block_num = (row//3)*3 + column//3

                    for key_number in list(cell_value):
                        self.step_list = copy.deepcopy(last_step_list)
                        self.update_step_list(['', '    第' + str(row+1) + '行第' + str(column+1) + '列，尝试数字' + str(key_number) + '。  （' + str(cell_value) + ' -> ' + str(key_number) + '）'])
                        last_step_list = copy.deepcopy(self.step_list)

                        self.update_sudoku_table(last_row_list)
                        self.sudoku_table.item(row, column).setText(key_number)
                        self.update_step_list()
                       
                        if (not self.fill_cell_possible_numbers(specified_row=row)) or (not self.fill_cell_possible_numbers(specified_column=column)) or (not self.fill_cell_possible_numbers(specified_block_num=block_num)):
                            self.step_list = copy.deepcopy(last_step_list)
                            self.update_step_list(['    尝试失败（尝试数字不合理）',])
                            last_step_list = copy.deepcopy(self.step_list)
                            continue

                        if self.solve_sudoku_with_basic_methods():
                            return(True)
                        else:
                            self.step_list = copy.deepcopy(last_step_list)
                            self.update_step_list(['    尝试失败（找不到最终解）',])
                            last_step_list = copy.deepcopy(self.step_list)
                            continue

        return(False)
    ## Solve Sudoku (end) ##

    ## Show Step (start) ##
    def show_step(self):
        """
        Update self.step_text, self.sudoku_table, show GUI message if exists.
        """
        self.step_text.setText('')

        for (i, step_dic) in enumerate(self.step_list):
            if (self.current_step == -1) or (i <= self.current_step):
                self.update_sudoku_table(step_dic['row_list'])
                self.update_step_text(step_dic['step_text'])
                self.show_gui_message(step_dic['message_text'])

    def update_sudoku_table(self, row_list):
        """
        Update self.sudoku_table.
        """
        for (row, column_list) in enumerate(row_list):
            for (column, cell_value) in enumerate(column_list):
                self.sudoku_table.item(row, column).setText(cell_value)

                if len(list(cell_value)) > 1:
                    self.sudoku_table.item(row, column).setFont(QFont('Times', 10, QFont.Black))
                    self.sudoku_table.item(row, column).setForeground(QBrush(QColor(0, 0, 0)))
                elif len(list(cell_value)) == 1:
                    self.sudoku_table.item(row, column).setFont(QFont('Times', 24, QFont.Black))

                    if self.step_list and (not self.step_list[0]['row_list'][row][column]):
                        self.sudoku_table.item(row, column).setForeground(QBrush(QColor(0, 255, 0)))
     
    def update_step_text(self, step_text_list):
        """
        Update self.step_text, self.sudoku_table, show GUI message if exists.
        """
        if step_text_list:
            for step_text in step_text_list:
                self.step_text.insertPlainText(str(step_text) + '\n')
                set_text_position(self.step_text, 'End')

    def show_gui_message(self, message_list):
        """
        Show GUI message.
        """
        if message_list:
            message_string = '\n'.join(message_list)
            QMessageBox.information(self, 'Sudoku Solver', message_string)
    ## Show Step (end) ##


################
# Main Process #
################
def main():
    app = QApplication(sys.argv)
    mw = mainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
