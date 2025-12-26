class Solution:
    def minWindow(self, s: str, t: str) -> str:
        l,have=0,0
        res=""
        min_len=float("inf")
        tmap,smap={},{}
        for ch in t:
            tmap[ch]=1+tmap.get(ch,0)
        need=len(tmap)
        for r in range(len(s)):
            if s[r] in tmap:
                smap[s[r]]=smap.get(s[r],0)+1
                if smap[s[r]]==tmap[s[r]]:
                    have+=1
            while have==need:
                if r-l+1<min_len:
                    min_len=r-l+1
                    res=s[l:r+1]
                if s[l] in tmap:
                    smap[s[l]]-=1
                    if smap[s[l]]<tmap[s[l]]:
                        have-=1
                l+=1
        return res
        