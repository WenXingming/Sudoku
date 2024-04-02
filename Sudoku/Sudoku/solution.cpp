 #include <iostream>
#include <fstream>
#include <sstream>

#include <vector>
using namespace std;

class Solution {
private:
	bool answer{ false };//用来递归时，判断是否找到了答案

public:
	//判断填入数字后数独是否合法（默认初始数独合法）
	bool isvalid(int row, int col, vector< vector<char> >& board) {
		//数组模拟哈希表
		char arrRow[10]{ 0 };//判断行的数组,arrRow[k] 保存 字符'k'出现的次数
		char arrCol[10]{ 0 };//判断列的数组,arrCol[k] 保存 字符'k'出现的次数
		char arrBox[10]{ 0 };//判断行的数组,arrBox[k] 保存 字符'k'出现的次数

		for (int i = 0; i < board.size(); i++) {
			//判断行符合
			if (board[row][i] != '.') {
				int index = board[row][i] - '0';//index 对于字符 board[row][i] 在数组中的下标
				if (arrRow[index] == 0) {
					arrRow[index] = 1;
				}
				else { return false; }
			}
			//判断列符合
			if (board[i][col] != '.') {
				int index = board[i][col] - '0';//index 对于字符 board[i][col] 在数组中的下标
				if (arrCol[index] == 0) {
					arrCol[index] = 1;
				}
				else { return false; }
			}
		}
		//判断九宫格符合
		//(row/3)*3,(col/3)*3是所在九宫格的起始位置
		int rowStart = (row / 3) * 3;
		int colStart = (col / 3) * 3;

		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				if (board[rowStart + i][colStart + j] != '.') {
					int index = board[rowStart + i][colStart + j] - '0';//index 对于字符 board[rowStart + i][colStart + j] 在数组中的下标
					if (arrBox[index] == 0) {
						arrBox[index] = 1;
					}
					else { return false; }
				}
			}
		}

		//经过了考验
		return true;
	}



	void solveSudoku(vector<vector<char>>& board) {
		backTracking(0, 0, board);
	}

	//对 board[row][col] 位置，插入数字
	void backTracking(int row, int col, vector<vector<char>>& board) {
		while (row != 9 && board[row][col] != '.') {
			row = row + (col + 1) / 9;
			col = (col + 1) % 9;
		}//找到空格，最后row可能出界了，所以递归退出条件放在下面

		if (row == 9) {
			answer = true;
			return;
		}//找到了答案,退出递归的条件

		for (char i = '1'; i <= '9'; i++)//填入数字,合法就转向下一格
		{
			board[row][col] = i;
			if (isvalid(row, col, board)) {
				backTracking(row + (col + 1) / 9, (col + 1) % 9, board);
			}
			else {continue;}
			//重点：回溯
			if (answer) return;//如果归来时已经找到了答案，就不用继续递归寻找答案（不能放在for头部，否则9归来时如果已经找到了答案，退出循环会被置为空格）
		}
		//重点：回溯
		board[row][col] = '.';//9归来时都没有找到答案，说明这个节点的1-9都不行，恢复为空，返回上一格
		return;
	}
};

// 函数用于读取数独文件内容并将其存储在二维向量中
vector<std::vector<char>> read_question_file(const std::string& filename) {
	vector<std::vector<char>> result;

	std::ifstream file(filename);
	if (!file.is_open()) {
		std::cerr << "Error: cannot open file " << filename << std::endl;
		exit(1);
	}
	
	std::string line;
	int indexLine = 0;
	while (std::getline(file, line)) {	
		// iss >> c 表达式将从 iss 字符串流中逐个读取字符，并将其存储到变量 c 中。
		// 当遇到空格时，它将被视为输入的分隔符，因此空格将被跳过（空格），并且不会存储到 chars 字符向量中
		vector<char> tmp;
		std::istringstream iss(line);
		char c;
		while (iss >> c) {
			tmp.push_back(c);
		}
		result.push_back(tmp);
	}
	return result;
}

// 输出解数独结果 board 到文件 result.txt
void write_answer_file(const vector<vector<char>>& board, string filePath) {
	// 将解数独结果写入文件 result.txt, 自动创建文件
	std::ofstream file(filePath);
	if (!file.is_open()) {
		std::cerr << "Error: cannot open file result.txt" << std::endl;
		exit(1);
	}
	for (int i = 0; i < board.size(); ++i) {
		for (int j = 0; j < board[0].size(); ++j)
			file << char(board[i][j]) << ' ';
		file << endl;
	}
}
int main(){
	// 读取数独题目：手动输入或从文件中读取
	/*vector< vector<char> > board = {
		{'8', '7', '2', '.', '9', '5', '.', '.', '1'},
		{'.', '5', '3', '.', '.', '8', '6', '.', '.'},
		{'4', '.', '.', '7', '1', '.', '2', '.', '8'},
		{'9', '4', '.', '.', '.', '.', '1', '.', '3'}, 
		{'.', '2', '.', '.', '.', '6', '.', '8', '4'},
		{'6', '.', '8', '.', '.', '.', '.', '.', '.'},
		{'.', '.', '.', '.', '.', '7', '.', '.', '.'},
		{'3', '.', '4', '8', '.', '.', '5', '.', '.'},
		{'7', '1', '5', '3', '2', '9', '8', '.', '6'}
	};*/
	vector< vector<char> > board = read_question_file("./tmp/question.txt");

	Solution s;
	s.solveSudoku(board);
	
	/*for(int i = 0; i < board.size(); ++i){
		for(int j = 0; j < board[0].size(); ++j)
			std::cout << char(board[i][j]) << ' ';
		std::cout << endl;
	}*/
	
	write_answer_file(board, "./tmp/answer.txt");
	std::cout << "The answer has been written to file ./tmp/answer.txt" << std::endl;
	//system("pause");
	return 0;
}

