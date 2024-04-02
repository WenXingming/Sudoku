 #include <iostream>
#include <fstream>
#include <sstream>

#include <vector>
using namespace std;

class Solution {
private:
	bool answer{ false };//�����ݹ�ʱ���ж��Ƿ��ҵ��˴�

public:
	//�ж��������ֺ������Ƿ�Ϸ���Ĭ�ϳ�ʼ�����Ϸ���
	bool isvalid(int row, int col, vector< vector<char> >& board) {
		//����ģ���ϣ��
		char arrRow[10]{ 0 };//�ж��е�����,arrRow[k] ���� �ַ�'k'���ֵĴ���
		char arrCol[10]{ 0 };//�ж��е�����,arrCol[k] ���� �ַ�'k'���ֵĴ���
		char arrBox[10]{ 0 };//�ж��е�����,arrBox[k] ���� �ַ�'k'���ֵĴ���

		for (int i = 0; i < board.size(); i++) {
			//�ж��з���
			if (board[row][i] != '.') {
				int index = board[row][i] - '0';//index �����ַ� board[row][i] �������е��±�
				if (arrRow[index] == 0) {
					arrRow[index] = 1;
				}
				else { return false; }
			}
			//�ж��з���
			if (board[i][col] != '.') {
				int index = board[i][col] - '0';//index �����ַ� board[i][col] �������е��±�
				if (arrCol[index] == 0) {
					arrCol[index] = 1;
				}
				else { return false; }
			}
		}
		//�жϾŹ������
		//(row/3)*3,(col/3)*3�����ھŹ������ʼλ��
		int rowStart = (row / 3) * 3;
		int colStart = (col / 3) * 3;

		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				if (board[rowStart + i][colStart + j] != '.') {
					int index = board[rowStart + i][colStart + j] - '0';//index �����ַ� board[rowStart + i][colStart + j] �������е��±�
					if (arrBox[index] == 0) {
						arrBox[index] = 1;
					}
					else { return false; }
				}
			}
		}

		//�����˿���
		return true;
	}



	void solveSudoku(vector<vector<char>>& board) {
		backTracking(0, 0, board);
	}

	//�� board[row][col] λ�ã���������
	void backTracking(int row, int col, vector<vector<char>>& board) {
		while (row != 9 && board[row][col] != '.') {
			row = row + (col + 1) / 9;
			col = (col + 1) % 9;
		}//�ҵ��ո����row���ܳ����ˣ����Եݹ��˳�������������

		if (row == 9) {
			answer = true;
			return;
		}//�ҵ��˴�,�˳��ݹ������

		for (char i = '1'; i <= '9'; i++)//��������,�Ϸ���ת����һ��
		{
			board[row][col] = i;
			if (isvalid(row, col, board)) {
				backTracking(row + (col + 1) / 9, (col + 1) % 9, board);
			}
			else {continue;}
			//�ص㣺����
			if (answer) return;//�������ʱ�Ѿ��ҵ��˴𰸣��Ͳ��ü����ݹ�Ѱ�Ҵ𰸣����ܷ���forͷ��������9����ʱ����Ѿ��ҵ��˴𰸣��˳�ѭ���ᱻ��Ϊ�ո�
		}
		//�ص㣺����
		board[row][col] = '.';//9����ʱ��û���ҵ��𰸣�˵������ڵ��1-9�����У��ָ�Ϊ�գ�������һ��
		return;
	}
};

// �������ڶ�ȡ�����ļ����ݲ�����洢�ڶ�ά������
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
		// iss >> c ���ʽ���� iss �ַ������������ȡ�ַ���������洢������ c �С�
		// �������ո�ʱ����������Ϊ����ķָ�������˿ո񽫱��������ո񣩣����Ҳ���洢�� chars �ַ�������
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

// ������������ board ���ļ� result.txt
void write_answer_file(const vector<vector<char>>& board, string filePath) {
	// �����������д���ļ� result.txt, �Զ������ļ�
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
	// ��ȡ������Ŀ���ֶ��������ļ��ж�ȡ
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

