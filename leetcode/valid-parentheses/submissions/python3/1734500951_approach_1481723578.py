class Solution:
    def isValid(self, s: str) -> bool:
        dictt={
            '{':'}',
            '[':']',
            '(':')'
        }
        st=[]
        for s1 in s:
            if s1 in dictt:
                st.append(s1)
            else:
                if st and s1==dictt[st[-1]]:
                    st.pop()
                else:
                    return False
        return not st


            



        