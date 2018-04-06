class StringUtils:

    @staticmethod
    def rreplace(string: str, old: str, new: str, occurrence: int):
        rsplitted_string = string.rsplit(old, occurrence)
        return new.join(rsplitted_string)
