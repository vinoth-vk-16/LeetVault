class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        st=[]
        dt={}
        seen=set()
        for i in range(len(s)):
            dt[s[i]]=i
        for i,val in enumerate(s):
            if val in seen:
                continue
            while st and st[-1]>val and dt[st[-1]]>i:
                rem=st.pop()
                seen.remove(rem)
            seen.add(val)
            st.append(val)
        return ''.join(st)
        
        