class Solution:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
        st=[]
        i=0
        for val in pushed:
            st.append(val)
            while st and i<len(popped) and st[-1]==popped[i]:
                st.pop()
                i+=1
        return not st

        