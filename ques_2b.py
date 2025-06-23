import numpy as np
#from numpy.random import choice
import random

class Alice:
    def __init__(self):
        self.past_play_styles = np.array([1,1])  
        self.results = np.array([1,0])           
        self.opp_play_styles = np.array([1,1])  
        self.points = 1

    def play_move(self):
        """
        Decide Alice's play style for the current round. Implement your strategy for 2a here.
         
        Returns: 
            0 : attack
            1 : balanced
            2 : defence

        """
        if self.results[-1] == 1:
            if self.points*11 < 5*self.results.size:
                return 0
            else:
                return 2
        elif self.results[-1] == 0.5:
            return 0
        else:
            return 1
        
    
    def observe_result(self, own_style, opp_style, result):
        """
        Update Alice's knowledge after each round based on the observed results.
        
        Returns:
            None
        """
        self.past_play_styles = np.append(self.past_play_styles, own_style)
        self.results = np.append(self.results, result)
        self.opp_play_styles = np.append(self.opp_play_styles, opp_style)
        self.points = self.points + result

class Bob:
    def __init__(self):
        # Initialize numpy arrays to store Bob's past play styles, results, and opponent's play styles
        self.past_play_styles = np.array([1,1]) 
        self.results = np.array([0,1])          
        self.opp_play_styles = np.array([1,1])   
        self.points = 1

    def play_move(self):
        """
        Decide Bob's play style for the current round.

        Returns: 
            0 : attack
            1 : balanced
            2 : defence
        
        """
        if self.results[-1] == 1:
            return 2
        elif self.results[-1] == 0.5:
            return 1
        else:  
            return 0
        
        
    
    def observe_result(self, own_style, opp_style, result):
        """
        Update Bob's knowledge after each round based on the observed results.
        
        Returns:
            None
        """ 
        self.past_play_styles = np.append(self.past_play_styles, own_style)
        self.results = np.append(self.results, result)
        self.opp_play_styles = np.append(self.opp_play_styles, opp_style)
        self.points = self.points + result
         

def simulate_round(alice, bob, payoff_matrix):
    """
    Simulates a single round of the game between Alice and Bob.
    
    Returns:
        None
    """

    alice_move = alice.play_move()
    bob_move = bob.play_move()

    P_alice = payoff_matrix[alice_move][bob_move][0]
    P_draw = payoff_matrix[alice_move][bob_move][1]
    P_bob = payoff_matrix[alice_move][bob_move][2]

    result = random.choices(population = [1, 0.5, 0], weights = [P_alice, P_draw, P_bob], k = 1)
    

    alice.observe_result(alice_move, bob_move, result[0])
    bob.observe_result(bob_move, alice_move, (1-result[0]))

    payoff_matrix[0][0][0] = bob.points/(alice.points + bob.points)
    payoff_matrix[0][0][2] = alice.points/(alice.points + bob.points)    


def monte_carlo(num_rounds):
    """
    Runs a Monte Carlo simulation of the game for a specified number of rounds.
    
    Returns:
        None
    """
    alice = Alice()
    bob = Bob()
    payoff_matrix = [[[1/2,0,1/2],[7/10,0,3/10],[5/11,0,6/11]],
                 [[3/10,0,7/10],[1/3,1/3,1/3],[3/10,1/2,1/5]],
                 [[6/11,0,5/11],[1/5,1/2,3/10],[1/10,4/5,1/10]]]
    for i in range(0, num_rounds):
        simulate_round(alice, bob, payoff_matrix)
    print(alice.points)
    print(bob.points)
    print(alice.points + bob.points)
    
 
# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    monte_carlo(num_rounds=pow(10,5))

payoff_matrix = [[[1/2,0,1/2],[7/10,0,3/10],[5/11,0,6/11]],
                 [[3/10,0,7/10],[1/3,1/3,1/3],[3/10,1/2,1/5]],
                 [[6/11,0,5/11],[1/5,1/2,3/10],[1/10,4/5,1/10]]]

def expected_points_optimal(tot_rounds):
    return 1 + max_exp(1, 1, tot_rounds -2, 2) #coz Bob will play defensive in third game

def max_exp(na, nb, rounds, bob_move): #seeing rounds after the two initial games
    #base case
    if rounds==0:
        return 0
    if exp_matrix[int(2*na)][int(2*nb)][rounds][bob_move] != -1:
        return exp_matrix[int(2*na)][int(2*nb)][rounds][bob_move]
    
    #Alice chooses to play Attack
    attack = 0
    payoff = payoff_matrix[0][bob_move]
    if bob_move == 0:
        attack += nb/(na+nb) * (1 + max_exp(na + 1, nb, rounds-1, 0)) #alice won
        attack += na/(na+nb) * (0 + max_exp(na, nb+1, rounds-1, 2))   #alice lost      
    else:
        score = 1
        for prob in range(0,3):
            attack += payoff[prob] * (score + max_exp(na + score, nb + 1- score, rounds -1, int(2*(1-score))))
            score -= 1/2
    
    #Alice chooses to Balance
    balance = 0
    payoff = payoff_matrix[1][bob_move]
    score = 1
    for prob in range(0,3):
        balance += payoff[prob] * (score + max_exp(na + score, nb + 1- score, rounds -1, int(2*(1-score))))
        score -= 1/2

    #Alice chooses to Defend
    defend = 0
    payoff = payoff_matrix[2][bob_move]
    score = 1
    for prob in range(0,3):
        defend += payoff[prob] * (score + max_exp(na + score, nb + 1- score, rounds -1, int(2*(1-score))))
        score -= 1/2

    #optimal solution
    exp_matrix[int(2*na)][int(2*nb)][rounds][bob_move] = max(attack, balance, defend)

    return exp_matrix[int(2*na)][int(2*nb)][rounds][bob_move]

def expected_points_greedy(tot_rounds):
    return 1 + greedy_exp(1, 1, tot_rounds-2, 2)

def greedy_exp(na, nb, rounds, bob_move): #seeing rounds after the two initial games
    #base case
    if rounds==0:
        return 0
    if greedy_matrix[int(2*na)][int(2*nb)][rounds][bob_move] != -1:
        return greedy_matrix[int(2*na)][int(2*nb)][rounds][bob_move]
    
    #Alice chooses to play Attack
    attack = 0
    payoff = payoff_matrix[0][bob_move]
    if bob_move == 0:
        attack += nb/(na+nb) * (1 + greedy_exp(na + 1, nb, rounds-1, 0)) #alice won
        attack += na/(na+nb) * (0 + greedy_exp(na, nb+1, rounds-1, 2))   #alice lost      
    else:
        score = 1
        for prob in range(0,3):
            attack += payoff[prob] * (score + greedy_exp(na + score, nb + 1- score, rounds -1, int(2*(1-score))))
            score -= 1/2
    
    #Alice chooses to Balance
    balance = 0
    payoff = payoff_matrix[1][bob_move]
    score = 1
    for prob in range(0,3):
        balance += payoff[prob] * (score + greedy_exp(na + score, nb + 1- score, rounds -1, int(2*(1-score))))
        score -= 1/2

    #Alice chooses to Defend
    defend = 0
    payoff = payoff_matrix[2][bob_move]
    score = 1
    for prob in range(0,3):
        defend += payoff[prob] * (score + greedy_exp(na + score, nb + 1- score, rounds -1, int(2*(1-score))))
        score -= 1/2

    #greedy solution
    if bob_move == 2: #bob won
        greedy_matrix[int(2*na)][int(2*nb)][rounds][bob_move] = balance
    if bob_move == 1: #draw
        greedy_matrix[int(2*na)][int(2*nb)][rounds][bob_move] = attack
    if bob_move == 0: #alice won
        if nb/(na+nb) > 6/11:
            greedy_matrix[int(2*na)][int(2*nb)][rounds][bob_move] = attack
        else:
            greedy_matrix[int(2*na)][int(2*nb)][rounds][bob_move] = defend

    return greedy_matrix[int(2*na)][int(2*nb)][rounds][bob_move]


T = 98
exp_matrix = [[[[-1 for _ in range(3)] for _ in range(T+1)] for _ in range(2*(T+2))] for _ in range(2*(T+2))]
greedy_matrix = [[[[-1 for _ in range(3)] for _ in range(T+1)] for _ in range(2*(T+2))] for _ in range(2*(T+2))]

eto = expected_points_optimal(T+2)
etg = expected_points_greedy(T+2)
print(eto)
print(etg)
