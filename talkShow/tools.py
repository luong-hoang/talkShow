class Tools:
    @staticmethod
    def md5(string):
        import hashlib
        encode = string.encode('utf')
        return hashlib.md5(encode).hexdigest()
