"""
This module contains some functions we previously defined.
"""

def cobb_douglas(l, k, A=1.01, alpha = 0.75):
    """
    This function computes the Cobb Douglas production function from labor and capital.
    """
    return A* l**alpha * k**(1-alpha)


def fibonacci(n):
    """
    This function computes the n-th Fibonacci number
    """
    if n in (0, 1):              
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)  

def threshold_morality(cost,benefit):
    """
    This function computes the threshold degree of morality
    allowing for cooperation in a social dilemma, 
    with a given individual cost and social benefit.
    """
    return cost/(cost+benefit)