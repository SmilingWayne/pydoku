from math import inf

from Utils import *

class Node(object):
    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.up, self.down, self.left, self.right = self, self, self, self

class ColumnNode(Node):
    def __init__(self, id):
        Node.__init__(self, self, id)
        self.row_count = 0


class DLX(object):
    def __init__(self):
        self.root = ColumnNode(0)

    def create_matrix(self, grid_str):
        """Creates an exact cover matrix from a sudoku grid"""
        root = self.root
        cols = [root]
        # Construct column headers as a doubly circular linked list
        # We'll be storing all the column headers in a list for easy access
        for i in range(324):
            c = ColumnNode(i + 1)
            c.right = root
            c.left = root.left
            root.left.right = c
            root.left = c
            cols.append(c)

        # These help us find which constraint should be filled in
        row_constraint = lambda x, k: 81 + (x // 9) * 9 + k
        col_constraint = lambda x, k: 162 + (x % 9) * 9 + k
        box_constraint = lambda x, k: 243 + (x // 27) * 27 + (x % 9) // 3 * 9 + k
        row_num = lambda x, k: x * 9 + k

        def _append_to_column(n):
            """Appends a row node at the end of a column"""
            c = n.column
            c.row_count += 1
            n.down = c
            n.up = c.up
            c.up.down = n
            c.up = n

        def _create_links(x, k):
            """Creates links for a row"""
            cell_node = Node(cols[x + 1], row_num(x, k))
            row_node = Node(cols[row_constraint(x, k)], row_num(x, k))
            col_node = Node(cols[col_constraint(x, k)], row_num(x, k))
            box_node = Node(cols[box_constraint(x, k)], row_num(x, k))

            # print(box_constraint(x, k))
            # Link all the nodes into a single row
            cell_node.right, cell_node.left = row_node, box_node
            row_node.right, row_node.left = col_node, cell_node
            col_node.right, col_node.left = box_node, row_node
            box_node.right, box_node.left = cell_node, col_node

            _append_to_column(cell_node)
            _append_to_column(row_node)
            _append_to_column(col_node)
            _append_to_column(box_node)


        for index, chr in enumerate(grid_str):
            if chr == '0':
                # Square is empty, add all possible values
                for k in range(9):
                    _create_links(index, k + 1)
            else:
                _create_links(index, ord(chr) - 48)

    def choose_least_column(self):
        """
        We use the S heuristic to minimize branching factor
        Returns the column with the least number of rows
        """
        c = None
        i = self.root.right
        s = inf

        while i != self.root:
            if i.row_count < s:
                c = i
                s = i.row_count
            i = i.right
        return c

    def cover(self, col):
        """Removes a column along with all rows that intersect said column"""
        col.right.left = col.left
        col.left.right = col.right
        i = col.down
        while i != col:
            # Iterate through nodes in row and unlink them
            j = i.right
            while j != i:
                j.down.up = j.up
                j.up.down = j.down
                j.column.row_count -= 1
                j = j.right
            i = i.down

    def uncover(self, col):
        """ Undo covering of a column """
        i = col.up
        while i != col:
            j = i.left
            while j != i:
                j.down.up = j
                j.up.down = j
                j.column.row_count += 1
                j = j.left
            i = i.up
        col.right.left = col
        col.left.right = col

    def search(self, solution):
        """ Search for a solution from a exact cover matrix """

        # No columns left, a solution is found
        if self.root == self.root.right:
            return solution, True

        c = self.choose_least_column()
        self.cover(c)

        i = c.down
        while i != c:
            solution.append(i)
            j = i.right
            while j != i:
                self.cover(j.column)
                j = j.right

            solution, found = self.search(solution)
            if found:
                return solution, True

            i = solution.pop()
            c = i.column
            j = i.left
            while j != i:
                self.uncover(j.column)
                j = j.left

            i = i.down

        self.uncover(c)
        return solution, False


class Sudoku(object):

    def __init__(self, grid_str):
        self.grid_str = grid_str
    
    @runtime_display
    def solve(self):
        solver = DLX()
        solver.create_matrix(self.grid_str)
        dlx_solution, found = solver.search([])
        return dlx_solution, found

    def Solve(self):
        dlx_solution, found = self.solve()  
        if not found:
            print('Solution not found')
            return
        solution = [0] * 81
        for i in dlx_solution:
            val = i.row % 9
            if val == 0:
                val = 9
            solution[(i.row - 1) // 9] = val

        cmd_Visualization("".join([str(i) for i in  solution]))


class Jigsaw_DLX(DLX):
    
    def __init__(self):
        DLX.__init__(self)

    # ABBBBBBCDAABBBCCCDAAACCCDDDAEACCFFDGAEEFFFDDGEEFFFFDHGEEHHHHHHGEEIHIIHGGIIIIIIGGG
    # 000006000907080016001300800200900000000053000000400000790014000350847020000100000
    
    def create_matrix(self, grid_str, region_str):
        """Creates an exact cover matrix from a sudoku grid"""
        root = self.root
        cols = [root]
        # Construct column headers as a doubly circular linked list
        # We'll be storing all the column headers in a list for easy access
        for i in range(324):
            c = ColumnNode(i + 1)
            c.right = root
            c.left = root.left
            root.left.right = c
            root.left = c
            cols.append(c)

        # These help us find which constraint should be filled in
        row_constraint = lambda x, k: 81 + (x // 9) * 9 + k
        col_constraint = lambda x, k: 162 + (x % 9) * 9 + k
        box_constraint = lambda devia, k: 243 + devia + k
        row_num = lambda x, k: x * 9 + k

        def _append_to_column(n):
            """Appends a row node at the end of a column"""
            c = n.column
            c.row_count += 1
            n.down = c
            n.up = c.up
            c.up.down = n
            c.up = n

        def _create_links(x, k, deviation):
            """Creates links for a row"""
            cell_node = Node(cols[x + 1], row_num(x, k))
            row_node = Node(cols[row_constraint(x, k)], row_num(x, k))
            col_node = Node(cols[col_constraint(x, k)], row_num(x, k))
            # print(box_constraint(deviation, k))
            box_node = Node(cols[box_constraint(deviation, k)], row_num(x, k))
            # print(row_num(x, k))
            # Link all the nodes into a single row
            cell_node.right, cell_node.left = row_node, box_node
            row_node.right, row_node.left = col_node, cell_node
            col_node.right, col_node.left = box_node, row_node
            box_node.right, box_node.left = cell_node, col_node

            _append_to_column(cell_node)
            _append_to_column(row_node)
            _append_to_column(col_node)
            _append_to_column(box_node)

        
        for index, chr in enumerate(grid_str):
            current_region = ord(region_str[index]) - 65
            # print(current_region)
           
            if chr == '0':
                # Square is empty, add all possible values
                for k in range(9):
                    _create_links(index, k + 1, current_region * 9)
            else:
                _create_links(index, ord(chr) - 48, current_region * 9)


class Jigsaw_Sudoku(object):

    def __init__(self, grid_str, region_str):
        self.grid_str = grid_str
        self.region_str = region_str

    @runtime_display
    def solve(self):
        solver = Jigsaw_DLX()
        solver.create_matrix(self.grid_str, self.region_str)
        dlx_solution, found = solver.search([])
        return dlx_solution, found
    
    def Solve(self):
        dlx_solution, found = self.solve()
        if not found:
            print('Solution not found')
            return
        
        solution = [0] * 81
        for i in dlx_solution:
            
            val = i.row % 9
            if val == 0:
                val = 9
            solution[(i.row - 1) // 9] = val
        cmd_Visualization("".join([str(i) for i in  solution]))



@runtime_display
def R():
    List_ = [
        "500000300020100070008000009040007000000821000000600010300000800060004020009000005",
"800000009040001030007000600000023000050904020000105000006000700010300040900000008",
"000070100000008050020900003530000000062000004094600000000001800300200009000050070",
"000006080000100200009030005040070003000008010000200600071090000590000004804000000",
"000056000050109000000020040090040070006000300800000002300000008002000600070500010",
"500000004080006090001000200070308000000050000000790030002000100060900080400000005",
"070200009003060000400008000020900010800004000006030000000000600090000051000700002",
"100080000005900000070002000009500040800010000060007200000000710000004603030000402",
"000900100000080007004002050200005040000100900000070008605000030300006000070000006",
"000001080030500200000040006200300500000008010000060004050000700300970000062000000",
"800000005040003020007000100000004000090702060000639000001000700030200040500000008",
"900000001030004070006000200050302000000060000000078050002000600040700030100000009",
"500000008030007040001000900020603000000725000000800060009000100070400030800000005",
"400000009070008030006000100050702000000065000000003020001000600080300070900000004",
"100006009007080030000200400000500070300001002000090600060003050004000000900020001",
"800000001050009040003000600070056000000980000000704020006000300090400050100000008",
"010000009005080700300700060004250000000000000000840200008007500600000030090000001",
"300000005020007040001000900080036000000028000000704060009000100070400020500000003",
"400000003080002060007000900010508000000701000000026050009000700020600080300000004",
"600005020040700000009080000010000302000000087000200104070400003500006000008090000",
"007002000500090400010600000400050003060100000002007000000000810900000306000080059",
"400000008050002090001000600070503000000060000000790030006000100020900050800000004",
"300000009010006050002000400070060000000701000000845070004000200060500010900000003",
"000000789000100036009000010200030000070004000008500100300020000005800090040007000",
"100000000006700020080030500007060030000500008000004900300800600002090070040000001",
"700000005040001030002000900060008000000946000000103080009000200010300040500000007",
"001020000300004000050600070080900005002003000400010000070000038000800069000000200",
"007580000000030000000076005400000020090000100003060008010600900006800003200000040",
"097000000301005000045000800003008400000020060000100009700004300000900001000060020",
"003700000050004000100020080900000012000000400080010090007300000200090006040005000",
"000000100600000874000007026030400000005090000100008002009050000200001008040300000",
"100000004020006090005000800030650000000372000000098070008000500060900020400000001",
"005300000800000020070010500400005300010070006003200080060500009004000030000009700",
"000002005006700400000009008070090000600400700010000080060300100300000002400005000",
"020000600400080007009000010005006000300040900010200000000700004000001050800090300",
"900000007030008040006000200010389000000010000000205010002000600080400030700000009",
"002400006030010000500008000007000002010000030900600400000007001000090080400200500",
"100300000020090400005007000800000100040000020007060003000400800000020090006005007",
    ]
    
    for i in List_:
        s = Sudoku(i)
        solution, found = s.solve()
   

if __name__ == "__main__":
    # R()
    killerSudoku = "ABCCDDEEEABBFGHHIIABBFGGJKILLMNNJJKOPPMQRSSOOTQQQRUSOVTTWWUUUVVXYYYYZZZZXaabbbccZ"
    number = [15, 24, 11, 5, 16, 17, 14, 10, 10, 21, 7, 15, 9, 10, 20, 10, 12, 15, 15, 17, 16, 18, 8, 10, 13, 32, 12, 13, 10]
    cage_idx = [0 for _ in range(81)]
    cage_start_val = {} # 统计这个cage所属的行开始的序号
    cage_dict = {}  # 统计这个cage的大小
    current_val = 324
    for idx, pos in enumerate(killerSudoku):
        if pos not in cage_dict:
            
            cage_dict[pos] = killerSudoku.count(pos)
            cage_start_val[pos] = current_val
            current_val += (number[ord(pos) - 65] if pos >= 'A' and pos <= 'Z' else number[ord(pos) - 97 + 26])
        if pos >= "A" and pos <= "Z":
            cage_idx[idx] = number[ord(pos) - 65]
            # cage_start_val[pos
        else:
            cage_idx[idx] = number[ord(pos) - 97 + 26]

    for idx, pos in enumerate(cage_idx):
        candidates = get_possible_candidates(cage_dict[killerSudoku[idx]], pos)
        print(candidates)
    for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZabc":
        print(f"{i} : {cage_start_val[i]}")
    

# killerSudoku = "ABCCDDFFFABBGHIIJJABBGHHKLJMMNOOKKLPQQNRSTTPPURRRSVTPWUUXXVVVWWYZZZZaaaaYbbcccdda"
#     ans = "946532781183974652527816943691287534378495216452163897765348129814629375239751468"
#     number = [15, 24, 11, 5, 16, 17, 14, 10, 10, 21, 7, 15, 9, 10, 20, 10, 12, 15, 15, 17, 16, 18, 8, 10, 13, 32, 12, 13, 10]
# 405个 1 - 24 ｜ 1 2 2 4 4 4 4 5 5 5 5 5