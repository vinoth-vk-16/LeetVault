class MyStack:

    def __init__(self):
        self.st=deque()
        

    def push(self, x: int) -> None:
        self.st.append(x)

    def pop(self) -> int:
        s=self.st.pop()
        return s

    def top(self) -> int:
        return self.st[-1]

    def empty(self) -> bool:
        return len(self.st)==0
        


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()