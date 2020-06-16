def _parseattr(obj, string, profound=0, called=0):
    if called <= profound:
        obj = getattr(obj, string)
        splitted = string.split('_')
        if len(splitted) > 1 and splitted[-1] == "id":
            called += 1
            return getattstr(obj, profound, called)
        if len(splitted) > 1 and splitted[-1] == "ids":
            called += 1
            return [getattstr(o, profound, called) for o in getattr(obj, string)]
        return getattr(obj, string)


def getattstr(obj, profound=0, called=0):
    fields = obj.fields_get_keys()
    vals = {f: _parseattr(obj, f, profound, called) for f in fields}
    return vals
