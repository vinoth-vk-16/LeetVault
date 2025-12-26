class MyHashMap:

    def __init__(self):
        self.arr=[]

    def put(self, key: int, value: int) -> None:
        for val in self.arr:
            if val[0]==key:
                val[1]=value
        self.arr.append([key,value])
        
        
    def get(self, key: int) -> int:
        for val in self.arr:
            if val[0]==key:
                return val[1]
        return -1
        

    def remove(self, key: int) -> None:
        arr1=[] 
        for i in range(0,len(self.arr)):
            if self.arr[i][0]==key:
                continue
            else:
                arr1.append(self.arr[i])
        self.arr=arr1

  


# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)