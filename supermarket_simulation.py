import pandas as pd
import random
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

#%%
# Read the transition matrix from the generated csv file
TRANSITION_MATRIX = pd.read_csv('data/transition_matrix.csv', index_col=0)

#%%
# deinfe the class for Customer
# Single customer that moves through the super market in a MCMC simulation

class Customer():
    def __init__(self, name, state):
        self.name = name
        self.state = state

    def __repr__(self):
        return f'Customer {self.name} in {self.state}'

    def next_state(self):
        '''
        Propagates the customer to the next state.
        Returns nothing.
        '''
        self.state = random.choices(['checkout', 'dairy', 'drinks', 'fruit', 'spices'], weights=TRANSITION_MATRIX.loc[self.state])
        self.state = self.state[0]

    def is_active(self):
        if self.state == 'checkout':
            return False
        else:
            return True

#%%
# Classe of supermarket declration
# Manages multiple customer instances that are currently in the market

class Supermarket():
    def __init__(self, market_name, opening, closing):
        self.market_name = market_name
        self.opening = opening   # opening time of the supermarket in string format
        self.closing = closing  # closing time of the Supermarket in the string format
        self.customers = []      # list of all customers
        self.current_time = 0
        self.index = 0           # time counter minute-wise
        self.customer_index = 0  # customer ID
        self.state = 0
        # delta time intervals [7:00, 7:01, ..7:59] : array of timesteps, T : minutely frequency (offset aliase
        self.dti = pd.date_range(self.opening, self.closing, freq="T").time

    def __repr__(self):
        return f'{len(self.dti)}'

    def is_open(self):
        if self.index <= len(self.dti) - 2:   # two minutes before the closing
            return datetime.strptime(self.opening, '%H:%M:%S') <= datetime.strptime(self.get_time(), '%H:%M:%S') <= datetime.strptime(self.closing, '%H:%M:%S')
            # returns true if the current time is between the opening and closing hour

    # current time in HH:MM format
    def get_time(self):
        self.current_time = self.dti[self.index]
        self.current_time = str(self.current_time)
        return self.current_time

    # returns all customers with the time  and id in CSV format
    def print_customer(self):
        return self.customers

    def next_minute(self):
        self.index +=1
        next_time = self.dti[self.index]

        for customers in self.customers:
            customer.next_state()

    #   randomly creates new customers
    def add_new_customers(self):
        self.state = random.choices(['dairy', 'drinks', 'fruit', 'spices'])
        self.state = self.state[0]
        self.customer_index += 1
        new_customer = Customer(self.customer_index, self.state)
        self.customers.append(new_customer)

    # rem
    def remove_existing_customer(self):
        for customer in self.customers:
            if not customer.is_active():
                self.customers.remove(customer)

#%%

if __name__ == "__main__":

    # Name of the super market : 'MarketRangers' a fancy exciting magical post-modern supermarket in wonderland
    # Simulation happens between 07:00:00 and 07:59:00

    supermarket = Supermarket('MarketRangers', '07:00:00', '07:59:00')
    market_rangers = pd.DataFrame()

    while supermarket.is_open():
        supermarket.add_new_customers()
        for customer in supermarket.customers:
            market_rangers = market_rangers.append({'timestamp': supermarket.get_time(),
                                                    'customer_no': str(customer.name),
                                                    'location':
                                                        str(customer.state),
                                                    }, ignore_index=True)
        supermarket.remove_existing_customer()
        supermarket.next_minute()

    market_rangers.set_index('timestamp', inplace=True)
    market_rangers.to_csv('output/simulated_market_table_average.csv')








#%%
