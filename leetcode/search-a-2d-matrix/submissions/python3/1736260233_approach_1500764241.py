class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        l=0
        r=len(matrix)-1
        while l<=r:
            mid=(l+r)//2
            print(matrix[mid])
            le=len(matrix[mid])-1
            if matrix[mid][le]<target:
                l=mid+1
            elif matrix[mid][0]>target:     
                r=mid-1
            else:
                if target in matrix[mid]:
                    return True
                break
        return False


        