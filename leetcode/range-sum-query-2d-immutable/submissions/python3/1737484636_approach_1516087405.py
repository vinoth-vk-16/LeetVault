class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        self.matrix=matrix
        for i in range(len(self.matrix)):
            for j in range(1,len(self.matrix[i])):
                self.matrix[i][j]=(self.matrix[i][j-1]+self.matrix[i][j])
        for j in range(len(self.matrix[0])):
            for i in range(1,len(self.matrix)):
                self.matrix[i][j]=(self.matrix[i-1][j]+self.matrix[i][j])
        print(self.matrix)

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        total = self.matrix[row2][col2]
        if row1 > 0:
            total -= self.matrix[row1 - 1][col2]
        if col1 > 0:
            total -= self.matrix[row2][col1 - 1]
        if row1 > 0 and col1 > 0:
            total += self.matrix[row1 - 1][col1 - 1]
        return total
        


# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)