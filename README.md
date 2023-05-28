# 食用指南🧭

## 棋盘表示

- 众所周知，一张棋盘可以有很多种表示方式，比如：
    - 通过 $9 \times 9$ 的二维列表传入；
    - 通过一个81个字符的字符串传入；
    - 用“0”表示没有填入的数字，用非0数表示棋盘已经有的数字
    - 用“.”表示没有填入的数字...
    - 这给我们编程造成了极大困扰。

- 为了减少类似的问题，我们人为规定，一副棋盘的表示方式为：一个长度为81的字符串。表示棋盘从左上角第一个格子开始，从左到右，从上到下依次读取棋盘数字组成的字符串。所有待定数字均按0填入。

- 此外，我们定义棋盘初始状态的盘面为“初盘”，解完的棋盘为“终盘”
- e.g. 因此，形如`900000001030004070006000200050302000000060000000078050002000600040700030100000009` 的初盘最终会形成字符串 `800000236169235487237684519394156728651728943782349165518493672926817354473562891` 表示为如下的数独终盘：

```
           初盘                              终盘
+-------+-------+-------+       +-------+-------+-------+
| 9 0 0 | 0 0 0 | 0 0 1 |       | 9 2 4 | 8 5 7 | 3 6 1 |
| 0 3 0 | 0 0 4 | 0 7 0 |       | 8 3 1 | 6 2 4 | 9 7 5 |
| 0 0 6 | 0 0 0 | 2 0 0 |       | 5 7 6 | 9 1 3 | 2 8 4 |
+-------+-------+-------+       +-------+-------+-------+   
| 0 5 0 | 3 0 2 | 0 0 0 |       | 7 5 8 | 3 4 2 | 1 9 6 |
| 0 0 0 | 0 6 0 | 0 0 0 |       | 4 1 3 | 5 6 9 | 7 2 8 |
| 0 0 0 | 0 7 8 | 0 5 0 |       | 2 6 9 | 1 7 8 | 4 5 3 |
+-------+-------+-------+       +-------+-------+-------+ 
| 0 0 2 | 0 0 0 | 6 0 0 |       | 3 9 2 | 4 8 5 | 6 1 7 |
| 0 4 0 | 7 0 0 | 0 3 0 |       | 6 4 5 | 7 9 1 | 8 3 2 |
| 1 0 0 | 0 0 0 | 0 0 9 |       | 1 8 7 | 2 3 6 | 5 4 9 |
+-------+-------+-------+       +-------+-------+-------+

```


## 代码功能🥰

- [backTrackSolver.py](./backTrackSolver.py): 借助基础回溯算法解数独问题；
- [BestFirstSearchSolver.py](./BestFirstSearchSolver.py): 基于Best-First-Search 搜索方法启发式地求解数独问题；
- [DLXSolver.py](./DLXsolver.py)：基于舞蹈链算法求解数独问题；
- [data.txt](./data.txt):基于 [Sudoku Explainer](https://sourceforge.net/projects/sudoku-explainer/) 软件生成的50个不同难度的数独难题。其中包含25简单题+15中等题+5较难题+5困难题，乱序排列。不同算法的效果可以参考解决所有50道难题的总时间进行。
- [WiseSearchSolver.py](WiseSearchSolver.py)：更加聪明的搜索。思路是在搜索前就对棋盘中一些备选数进行删除（Pruning）；参考[Norvig的实现方法](http://www.norvig.com/sudoku.html);
- [Utils.py](./Utils.py)：一些可能（实际上没怎么）用到的脚本工具。

## 调试技巧

- 在每个文件（除了utils.py），都有一些注释中含有 "TODO"，这些注释下一些行可以取消/增加可视化棋盘的过程。
- 直接执行py文件获取结果。



## Reference & Resources

- [https://www.ocf.berkeley.edu/~arel/sudoku/main.html](https://www.ocf.berkeley.edu/~arel/sudoku/main.html): 数独生成算法
- [https://anhminhtran235.github.io/sudoku-solver-visualizer/](https://anhminhtran235.github.io/sudoku-solver-visualizer/)： 几种数独求解算法的可视化
- [https://blog.csdn.net/zhouchangyu1221/article/details/88774110](https://blog.csdn.net/zhouchangyu1221/article/details/88774110)：如何对标准数独问题进行建模
- [http://www.norvig.com/sudoku.html](http://www.norvig.com/sudoku.html)：“求解所有的数独”：算法介绍和表示
- [https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf)：经典的舞蹈链算法
- [https://www.kaggle.com/datasets/bryanpark/sudoku](https://www.kaggle.com/datasets/bryanpark/sudoku)：Kaggle上的百万级数独题库
- [https://www.kaggle.com/datasets/informoney/4-million-sudoku-puzzles-easytohard](https://www.kaggle.com/datasets/informoney/4-million-sudoku-puzzles-easytohard)：按照难度区分的4百万级别数独题库。但是有一些棋盘没有唯一解。
- [https://zhuanlan.zhihu.com/p/448969860](https://zhuanlan.zhihu.com/p/448969860)：数独回溯算法的时间复杂度计算（Best-First-Search的复杂度与之相同，但是最坏时间复杂度低于一般的回溯）
- [https://stackoverflow.com/questions/37715983/complexity-of-dancing-links](https://stackoverflow.com/questions/37715983/complexity-of-dancing-links): 舞蹈链算法的时间复杂度计算
- [https://stackoverflow.com/questions/6924216/how-to-generate-sudoku-boards-with-unique-solutions?rq=1](https://stackoverflow.com/questions/6924216/how-to-generate-sudoku-boards-with-unique-solutions?rq=1)：如何生成一个数独
- [https://stackoverflow.com/questions/500607/what-are-the-lesser-known-but-useful-data-structures](https://stackoverflow.com/questions/500607/what-are-the-lesser-known-but-useful-data-structures)：一些经典的遗产：数据结构篇