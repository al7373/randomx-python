
class Pointer:
    def __init__(self, instance, accessor=0):
        self._instance = instance
        self._accessor = accessor

    def getValue(self):
        if type(self._instance) is list:
            return self._instance[self._accessor]
        return getattr(self._instance, self._accessor)

    def setValue(self, value):
        if type(self._instance) is list:
            self._instance[self._accessor] = value
            return
        setattr(self._instance, self._accessor, value)

    def getAccessor(self):
        return self._accessor

