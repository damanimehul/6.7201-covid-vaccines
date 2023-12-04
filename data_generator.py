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
            population_data  = pd.DataFrame([population],columns=[state_list[i]]) 
        else: 
            state_data[state_list[i]] = case_numbers 
            population_data[state_list[i]] = [population] 
    # convert to dataframe
    print(f'Total population: {total_population}') 
    return state_data, population_data, total_population 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate COVID-19 data for US states')
    parser.add_argument('--name', type=str, default='covid_data')
    parser.add_argument('--num_weeks', type=int, default=20,
                        help='Number of weeks to generate data for')
    parser.add_argument('--num_states', type=int, default=50,
                        help='Number of states to generate data for')
    parser.add_argument('--initial_vaccine_capacity', type=float, default=0.01, help='Vaccine capacity in terms of proportion of total population (0.1 = 10 percent of population)') 
    parser.add_argument('--vaccine_capacity_increase', type=float, default=0.05, help='Increase in vaccine capacity per week')  
    args = parser.parse_args()
    state_data,population_data,total_population = generate_state_case_data(args.num_weeks,args.num_states)
    # save to csv with state names as columns, use timestamp in filename
    #use timestamp in filename
    state_data.to_csv(f'case_data_{args.name}.csv',index=False) 
    population_data.to_csv(f'population_data_{args.name}.csv',index=False) 

    vaccines_available = [] 
    vaccine_coeff = args.initial_vaccine_capacity
    for i in range(args.num_weeks): 
        vaccines_available.append(int(vaccine_coeff*total_population)) 
        vaccine_coeff  *= (1+args.vaccine_capacity_increase) 
    # save to csv 
    vaccine_data = pd.DataFrame(vaccines_available,columns=['vaccines_available'])
    vaccine_data.to_csv(f'vaccine_data_{args.name}.csv',index=False) 
    
    
    



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
