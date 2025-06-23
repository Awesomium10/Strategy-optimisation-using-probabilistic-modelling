import numpy as np
import random

class Alice:
    def __init__(self):
        self.past_play_styles = np.array([1,1])  
        self.results = np.array([1,0])           
        self.opp_play_styles = np.array([1,1])  
        self.points = 1
        self.wins = 1

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
        if result == 1:
            self.wins = self.wins + 1
       

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

def estimate_tau(T):
    """

    Estimate the expected value of the number of rounds taken for Alice to win 'T' rounds.
    Your total number of simulations must not exceed 10^5.

    Returns:
        Float: estimated value of E[tau]
    """
    E_tau = 0
    tau = 0
    alice = Alice()
    bob = Bob()
    payoff_matrix = [[[1/2,0,1/2],[7/10,0,3/10],[5/11,0,6/11]],
                 [[3/10,0,7/10],[1/3,1/3,1/3],[3/10,1/2,1/5]],
                 [[6/11,0,5/11],[1/5,1/2,3/10],[1/10,4/5,1/10]]]
    for i in range (0, 1000):
        while (alice.wins < T):
            simulate_round(alice, bob, payoff_matrix)
        tau = tau + alice.points + bob.points 
        alice=Alice()
        bob=Bob()
    E_tau = tau/(1000)

    return E_tau

E = estimate_tau(95)       
print(E)