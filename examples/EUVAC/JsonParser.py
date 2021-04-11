class JsonParser:
    @staticmethod
    def findPathSafe(node, names):
        if not isinstance(names, list):
            raise ValueError("Names must be a list.")
        result = node
        for i in names:
            if not i in result:
                return None
            result = result[i]
        return result

    @staticmethod
    def findPath(node, names):
        result = node
        for i in names:
            result = result[i]
        return result
