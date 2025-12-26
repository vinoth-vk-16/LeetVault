class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        st=[]
        fin=""
        for val in s:
            if val=="(":
                st.append(val)
                if len(st)>1:
                    fin+="("
            elif val==")"and len(st)>1:
                a=st.pop()
                fin+=(")")
            else:
                st.pop()
        return fin
                
        