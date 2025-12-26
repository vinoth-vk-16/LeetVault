class Solution:
    def calculate(self, s: str) -> int:
        op=["*","+","-","/"]
        fin=0
        st=deque()
        i=0
        n=0
        sign='+'
        while i<len(s):
            ch=s[i]
            if ch.isdigit():
                n=n*10 +int(ch)
            if ch in op or i == len(s) - 1:
                if sign=="+":
                    st.append(n)
                elif sign=='-':
                    st.append(-n)
                elif sign=='*':
                    st.append(st.pop()*n)
                elif sign=='/':
                    st.append(int(st.pop()/n))
                n=0
                sign=ch
            i+=1
        return sum(st)

            


                

                
        