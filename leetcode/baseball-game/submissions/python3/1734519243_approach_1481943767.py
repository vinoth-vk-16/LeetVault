class Solution:
    def calPoints(self, operations: List[str]) -> int:
        st=deque()
        for val in operations:
            if val=='+':
                val1=st[-1]+st[-2]
                st.append(val1)
            elif val=='D':
                val1=2*st[-1]
                st.append(val1)
            elif val=='C':
                st.pop()
            else:
                st.append(int(val))
        return sum(st)
        