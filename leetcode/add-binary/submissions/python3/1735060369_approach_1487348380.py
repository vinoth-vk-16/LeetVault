class Solution:
    def addBinary(self, a: str, b: str) -> str:
        fin=str(bin(int(a,2)+int(b,2)))
        return fin[2:]
        
        