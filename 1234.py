# 1. on CheckiO your solution should be a function
# 2. the function should return the right answer, not print it.

def say_hi(name: str, age: int) -> str:
    """
        Hi!
    """
    # your code here
    return "Hi. My name is " + name + "and I'm " + age + " years old"

if __name__ == '__main__':

    #These "asserts" using only for self-checking and not necessary for auto-testing

    print('Done. Time to Check.')
