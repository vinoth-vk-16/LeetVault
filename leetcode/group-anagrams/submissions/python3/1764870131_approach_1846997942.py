class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        df={}
        i=0
        arr=[]
        for val in strs:
            s_val="".join(sorted(val))
            if s_val in df:
                arr[df[s_val]].append(val)
            else:
                df[s_val]=i
                arr.append([])
                arr[i].append(val)
                i+=1
        return arr
        