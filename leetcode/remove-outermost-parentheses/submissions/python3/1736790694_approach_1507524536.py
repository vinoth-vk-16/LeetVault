class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        a=0
        fin=""
        for val in s:
            if val=="(":
                a+=1
                if a>1:
                    fin+=val
            elif val==")":
                a-=1
                if a>0:
                    fin+=val
        return fin
        