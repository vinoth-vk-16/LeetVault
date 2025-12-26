class Solution:
    def kthCharacter(self, k: int) -> str:
        w="a"
        def rec(w,k):
            if len(w)>=k:
                return w[k-1]
            for c in w:
                nc=chr(ord(c)+1) if c != "z" else "a"
                w+=nc
            
            l=rec(w,k)
            return l
        fin=rec(w,k)
        return fin
        
        


