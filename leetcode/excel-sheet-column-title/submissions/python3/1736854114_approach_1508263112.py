class Solution:
    def convertToTitle(self, columnNumber: int) -> str:
        l=list(string.ascii_uppercase)
        mapp={}
        i=0
        res=[]
        for val in l:
            i+=1
            mapp[i]=val
        while columnNumber>0:
            columnNumber-=1
            rem=columnNumber%26+1
            res.append(mapp[rem])
            columnNumber//=26
        return "".join(res[::-1])