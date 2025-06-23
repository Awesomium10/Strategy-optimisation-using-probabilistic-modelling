import math 
"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
M=1000000007

def mod_add(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a+b)%M

def mod_multiply(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a*b)%M

def mod_divide(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return mod_multiply(a, pow(b, M-2, M))

def mod_factorial(a):
    if a==1:
        return mod_multiply(a,1)
    else:
        return mod_multiply(a, mod_factorial(a-1))

# Problem 1a
def calc_prob(alice_wins, bob_wins):
    """
    Returns:
        The probability of Alice winning alice_wins times and Bob winning bob_wins times will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.
    """
    #dynamic approach
    a = alice_wins
    b = bob_wins
    Prob_AA = [[0 for _ in range(b)] for _ in range(a)] #probability with Attack - Attack strategies
    for i in range(b):
        Prob_AA[0][i] = pow(mod_factorial(i+1), M-2, M)
    for i in range(a):
        Prob_AA[i][0] = pow(mod_factorial(i+1), M-2, M)
    for i in range(1, a):
        for j in range(1, b):
            Prob_AA[i][j] = mod_add(mod_multiply(Prob_AA[i-1][j] ,mod_divide((j+1),(i+j+1))) , mod_multiply(Prob_AA[i][j-1] , mod_divide((i+1),(i+j+1))))     
    return Prob_AA[a-1][b-1]
    
    
# Problem 1b (Expectation)      
def calc_expectation(t): #always zero 
    """
    Returns:
        The expected value of \sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    #return 0
    E = 0
    for i in range(1,t):
        E = mod_add(E,mod_multiply((2*i - t), calc_prob(i, t-i)))
    return E


# Problem 1b (Variance)
def calc_variance(t):
    """
    Returns:
        The variance of \sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    V = 0
    for i in range(1,t):
        V = mod_add(V,mod_multiply(pow((2*i - t), 2, M), calc_prob(i, t-i)))
    return V
    
A = calc_prob(98,88)
print(A)
E = calc_expectation(88)
print(E)
V = calc_variance(88)
print(V)
