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

# Problem 3b

payoff_matrix = [[[1/2,0,1/2],[7/10,0,3/10],[5/11,0,6/11]],
                 [[3/10,0,7/10],[1/3,1/3,1/3],[3/10,1/2,1/5]],
                 [[6/11,0,5/11],[1/5,1/2,3/10],[1/10,4/5,1/10]]]

def optimal_strategy(na, nb, tot_rounds):
    """
    Calculate the optimal strategy for Alice maximize her points in the future rounds
    given the current score of Alice(na) and Bob(nb) and the total number of rounds(tot_rounds).
    
    Return the answer in form of a list [p1, p2, p3],
    where p1 is the probability of playing Attacking
    p2 is the probability of playing Balanced
    p3 is the probability of playing Defensive
    """
    max_exp(na, nb, tot_rounds - 2)
    if opt_matrix[2*na][2*nb][tot_rounds - 2] == 0:
        return [1,0,0]
    elif opt_matrix[2*na][2*nb][tot_rounds - 2] == 1:
        return [0,1,0]
    elif opt_matrix[2*na][2*nb][tot_rounds - 2] == 2:
        return [0,0,1]

def expected_points(tot_rounds):
    """
    Given the total number of rounds(tot_rounds), calculate the expected points that Alice can score after the tot_rounds,
    assuming that Alice plays optimally.

    Return : The expected points that Alice can score after the tot_rounds.
    """
    return 1 + max_exp(1, 1, tot_rounds - 2)

def max_exp(na, nb, rounds):  #the rounds here are 2 less than the total T
    
    #Base cases
    if rounds==0:
        return 0
    #we can avoid recomputation as the exp_matrix is initialised as -1
    if exp_matrix[int(2*na)][int(2*nb)][rounds] != -1:
        return exp_matrix[int(2*na)][int(2*nb)][rounds]

    #Alice chooses to play Attack
    attack = 0
    payoff = payoff_matrix[0]
    bob_strat = 0
    attack += 1/3 * nb/(na+nb) * (1 + max_exp(na + 1, nb, rounds-1)) #alice won
    attack += 1/3 * na/(na+nb) * (0 + max_exp(na, nb+1, rounds-1))   #alice lost      
    for bob_strat in range(1,3):
        score = 1
        for prob in range(0,3):
            attack += 1/3 * payoff[bob_strat][prob] * (score + max_exp(na + score, nb + 1- score, rounds -1))
            score -= 1/2

    #Alice chooses to Balance
    balance = 0
    payoff = payoff_matrix[1]
    for bob_strat in range(0,3):
        score = 1
        for prob in range(0,3):
            balance += 1/3 * payoff[bob_strat][prob] * (score + max_exp(na + score, nb + 1- score, rounds -1))
            score -= 1/2

    #Alice chooses to Defend
    defend = 0
    payoff = payoff_matrix[2]
    for bob_strat in range(0,3):
        score = 1
        for prob in range(0,3):
            defend += 1/3 * payoff[bob_strat][prob] * (score + max_exp(na + score, nb + 1- score, rounds -1))
            score -= 1/2

    #I will store these expectations in a 3D matrix exp_matrix
    #since the points can be in 0.5, need to convert into int as in float 
    exp_matrix[int(2*na)][int(2*nb)][rounds] = max(attack, balance, defend)
    opt_matrix[int(2*na)][int(2*nb)][rounds] = [attack, balance, defend].index(exp_matrix[int(2*na)][int(2*nb)][rounds])

    return exp_matrix[int(2*na)][int(2*nb)][rounds] 

T = 98 #input T as total games minus 2 (lol I can just modify my code but kaun kare :P)
exp_matrix = [[[-1 for _ in range(T+1)] for _ in range(2*(T+2))] for _ in range(2*(T+2))]
opt_matrix = [[[-1 for _ in range(T+1)] for _ in range(2*(T+2))] for _ in range(2*(T+2))]

et = expected_points(T+2)
print(et)
print(optimal_strategy(15, 1, 77))