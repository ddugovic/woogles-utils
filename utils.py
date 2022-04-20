import inflect

def plural(noun, count):
    return inflect.engine().plural(noun, count)
