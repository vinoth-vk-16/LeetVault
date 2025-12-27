class Solution:
    def isValid(self, s: str) -> bool:
        st=deque()
        mapp={
            "]":"[",
            "}":"{",
            ")":"("
        }
        for val in s:
            if st and val in mapp and st[-1]==mapp[val]:
                st.pop()
            else:
                st.append(val)
        return len(st)==0
        