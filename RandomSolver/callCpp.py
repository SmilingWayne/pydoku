from ctypes import *
from callC import runtime_display

@runtime_display
def run():
    func = cdll.LoadLibrary('./Sudoku/RandomSolver/DLXsolver.so')
    func.SolveSudoku.restype = c_char_p
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
    for p in List_:
        rst = str(func.SolveSudoku(bytes(p, encoding="utf-8")), "utf-8" )

if __name__ == "__main__":
    run()