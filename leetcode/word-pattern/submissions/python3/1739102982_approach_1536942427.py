class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        dt={}
        w_m={}
        pattern=list(pattern)
        s=s.split(" ")
        if len(s)!=len(pattern):
            return False
        for i in range(len(pattern)):
            if pattern[i] not in dt:
                if s[i] in w_m:
                    return False
                dt[pattern[i]]=s[i]
                w_m[s[i]]=pattern[i]
                    
            else:
                if s[i]!=dt[pattern[i]]:
                    return False
        return True

        