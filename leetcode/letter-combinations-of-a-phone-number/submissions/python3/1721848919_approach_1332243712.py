class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        ph={2:['a','b','c'],3:['d','e','f'],4:['g','h','i'],5:['j','k','l'],6:['m','n','o'],7:['p','q','r','s'],8:['t','u','v'],9:['w','x','y','z']}
        dig=[]
        for char in digits:
            dig.append(int(char))
        stored_val=[]
        for num in dig:
            cur_val=ph[num]
            if not stored_val:
                stored_val.extend(cur_val)
            else:
                new_combinations = []
                for exval in stored_val:
                    for cv in cur_val:
                        new_combinations.append(exval+cv)
                stored_val= new_combinations
        return(stored_val)


        
