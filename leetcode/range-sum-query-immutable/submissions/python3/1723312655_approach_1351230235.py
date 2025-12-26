class NumArray(object):

    def __init__(self, nums):
        self.nums=nums

    def sumRange(self, left, right):
        """summ=0
        sum1=0
        for i in range (0,right+1):
            if(i<left):
                sum1+=self.nums[i]
            summ+=self.nums[i]
        print(summ,sum1)
        return summ-sum1"""
        return sum(self.nums[left:right+1])


        


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)