class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        min_len=999
        v=""
        pref=""
        for x in strs:
            if len(x)<min_len:
                min_len=len(x)  
        for i in range(0,min_len):
            v = [s[i] for s in strs]# idhu first element elathayu oru list la podum , list comprehension aama
            print(v)
            are_similar = all(p==v[0] for p in v)#boolean function idhu 
            if are_similar:
                pref+=v[0]
            else:
                break
        return pref               
