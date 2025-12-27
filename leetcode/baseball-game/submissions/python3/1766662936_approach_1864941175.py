from collections import deque
class Solution:
    def calPoints(self, operations: List[str]) -> int:
        st=deque()
        exp=["C","D","+"]
        for val in operations:
            if val not in exp:
                st.append(int(val))
            elif val=="+":
                st.append(st[-1]+st[-2])
            elif val=="C":
                st.pop()
            elif val=="D":
                st.append(st[-1]*2)
        
        return sum(st)

                

        