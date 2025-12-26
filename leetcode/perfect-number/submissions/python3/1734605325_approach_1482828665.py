class Solution:
    def checkPerfectNumber(self, num: int) -> bool:
        if num <= 1:
            return False 
        
        val = 1  
        limit = int(num**0.5)
        
        for i in range(2, limit + 1):  
            if num % i == 0:  
                val += i
                if i != num // i:  
                    val += num // i
        
        return val==num
