class JsonParser:
    @staticmethod
    def find_path_safe(node, names):
        if not isinstance(names, list):
            raise ValueError("Names must be a list.")
        result = node
        for i in names:
            if i not in result:
                return None
            result = result[i]
        return result

    @staticmethod
    def find_path(node, names):
        result = node
        for i in names:
            result = result[i]
        return result
