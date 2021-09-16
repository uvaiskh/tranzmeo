
class MovingTotal:
    def __init__(self):
        """stores all the numbers"""
        self.elements = list()
        '''stores total of consecutive elements'''
        self.total = list()

    def append(self, numbers):
        """slice last two elements in list if any"""
        pre = self.elements[:-3:-1]
        '''concatenate last two elements and new list'''
        pro_list = pre+numbers
        if len(pro_list) >= 3:
            '''for n number there will be n-2 totals'''
            for i in range(len(pro_list)-2):
                self.total.append(sum(pro_list[i:i+3]))
        self.elements = self.elements + numbers

    def contains(self, total):
        if total in self.total:
            return True
        return False


if __name__ == "__main__":
    movingtotal = MovingTotal()
    movingtotal.append([1, 2, 3, 4])
    print("contains 6: ", movingtotal.contains(6))
    print("contains 9: ", movingtotal.contains(9))
    print("contains 12: ", movingtotal.contains(12))
    print("contains 7: ", movingtotal.contains(7))
    movingtotal.append([5])
    print("contains 6: ", movingtotal.contains(6))
    print("contains 9: ", movingtotal.contains(9))
    print("contains 12: ", movingtotal.contains(12))
    print("contains 7: ", movingtotal.contains(7))

