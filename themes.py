import random

def theme_choice():
    """
    return : tuple with two different int in [0,5]
    """
    n = random.randint(0,5)
    m = random.randint(0,5)
    while n == m:
        m = random.randint(0,5)
    return n,m