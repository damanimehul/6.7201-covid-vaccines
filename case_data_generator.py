import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd 
import argparse 

def single_state_data(num_weeks,population=None): 
    mean_value = np.random.randint(0,20) 
    variance_value = np .random.randint(6,50) 
    peak_proportion = np.random.uniform(0.01,0.05)
    normal_distribution = norm(loc=mean_value, scale=np.sqrt(variance_value)) 
    if population is None:
        population = np.random.randint(50000,1000000)
    multiplier = (population*peak_proportion)/normal_distribution.pdf(mean_value)  
    case_numbers = [] 
    for i in range(num_weeks): 
        x_c = i 
        pdf_at_x_c = normal_distribution.pdf(x_c) 
        case_numbers.append(int(pdf_at_x_c * multiplier))
    return case_numbers, population

def generate_state_case_data(num_weeks,num_states=50): 
    #list of US States abbreviated 
    state_list = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ]
    num_states = len(state_list) 
    total_population = 0
    for i in range(num_states): 
        case_numbers, population = single_state_data(num_weeks) 
        total_population += population 
        if i == 0: 
            # create panda dataframe
            state_data = pd.DataFrame(case_numbers,columns=[state_list[i]]) 
        else: 
            state_data[state_list[i]] = case_numbers 
    # convert to dataframe
    print(f'Total population: {total_population}') 
    return state_data, total_population 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate COVID-19 data for US states')
    parser.add_argument('--num_weeks', type=int, default=20,
                        help='Number of weeks to generate data for')
    parser.add_argument('--num_states', type=int, default=50,
                        help='Number of states to generate data for')
    args = parser.parse_args()
    state_data,total_population = generate_state_case_data(args.num_weeks,args.num_states)
    # save to csv with state names as columns, use timestamp in filename
    #use timestamp in filename
    state_data.to_csv(f'covid_data_{total_population}_population_{args.num_weeks}_weeks_{args.num_states}_states.csv',index=True) 
    
    



# # Define mean and variance
# mean_value = 10
# variance_value = 3

# # Generate normal distribution
# normal_distribution = norm(loc=mean_value, scale=np.sqrt(variance_value))

# # Evaluate PDF at x=c
# x_c = 5
# pdf_at_x_c = normal_distribution.pdf(x_c)

# # Plot the PDF
# x_values = np.linspace(mean_value - 3 * np.sqrt(variance_value), mean_value + 3 * np.sqrt(variance_value), 1000)
# pdf_values = normal_distribution.pdf(x_values)

# plt.plot(x_values, pdf_values, label=f'N({mean_value}, {variance_value}) PDF')
# plt.scatter(x_c, pdf_at_x_c, color='red', label=f'PDF at x={x_c}')
# plt.title('Normal Distribution PDF')
# plt.xlabel('x')
# plt.ylabel('Probability Density')
# plt.legend()
# plt.show()

# print(f'PDF at x={x_c}: {pdf_at_x_c}')
