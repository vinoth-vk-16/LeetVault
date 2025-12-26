class Solution:
    def decodeString(self, s: str) -> str:
        st=[]
        for val in s:
            if val!="]":
                st.append(val)
            else:
                v=""
                v1=""
                while st and st[-1].isalpha():
                    v=st.pop()+v
                if st[-1]=="[":
                    st.pop()
                while st and st[-1].isdigit():
                    v1=st.pop()+v1
                st.append(int(v1)*v)
        return "".join(st)

        
        