class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        st=deque()
        st1=deque()
        for val in s:
            if st and val=="#":
                st.pop()
            else:
                if val!="#":
                    st.append(val)
        for val in t:
            if st1 and val=="#":
                st1.pop()
            else:
                if val!="#":
                    st1.append(val)
        return st1==st
        