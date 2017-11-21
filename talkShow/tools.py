class Tools:
    @staticmethod
    def md5(string):
        import hashlib
        encode = string.encode('utf')
        return hashlib.md5(encode).hexdigest()

    @staticmethod
    def list_empty_value(li, mode):
        if mode == 'int':
            func = int
            checker = 0
        elif mode == 'str':
            checker = ''
        elif mode == 'bool':
            checker = False
        else:
            checker = False

        for i in range(len(li)):
            if checker is None or li[i] == checker:
                return True
        return False

    @staticmethod
    def list_duplicated(li, ignore_empty=True):
        length = len(li)
        # 0 ---> len(li)
        for i in range(length):
            if ignore_empty and int(li[i]) == 0:
                continue
            checker = li[i]
            for j in range(i + 1, length):
                if checker == li[j]:
                    return True
        return False
