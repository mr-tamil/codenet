def Process():
    from . import Process as process
    print(type(process))
    print(dir(process), 10)
    return process

def Others():
    from . import Other as others
    return others
