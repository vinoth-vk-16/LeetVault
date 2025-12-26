class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        st=[]
        for val in tokens:
            if len(st)>=2 and val=='+':
                n2=st.pop()
                n1=st.pop()
                st.append(n1+n2)
                
            elif len(st)>=2 and val=='/':
                n2=st.pop()
                n1=st.pop()
                st.append(int(n1/n2))
                
            elif len(st)>=2 and val=='*':
                n2=st.pop()
                n1=st.pop()
                st.append(n1*n2)
                
            elif len(st)>=2 and val=='-':
                n2=st.pop()
                n1=st.pop()
                st.append(n1-n2)
                
            else:
                st.append(int(val))
                
        return st[0]
  