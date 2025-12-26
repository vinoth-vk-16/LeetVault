class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        s1=list(s1)
        s1.sort()
        if len(s2)<len(s1):
            return False
        l,r=0,len(s1)-1
        win=list(s2[:len(s1)])
        while r<len(s2):
            if sorted(win)==s1:
                return True
            r+=1
            if r==len(s2):
                break
            win.pop(0)
            win.append(s2[r])
        return False

        