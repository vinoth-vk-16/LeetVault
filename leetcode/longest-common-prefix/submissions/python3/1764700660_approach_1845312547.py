class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        df={}
        max_v = len(strs[0])
        for i in range(0,len(strs)):
            if i == 0:
                df = {idx: ch for idx, ch in enumerate(strs[0])}
                

            else:
                temp=0
                for val in range(0,len(strs[i])):
                    if val in df and df[val]==strs[i][val]:
                        temp+=1
                    else:
                   
                        break
                max_v = min(max_v, temp)  

                if max_v == 0:
                    return ""

        return strs[0][:max_v]


