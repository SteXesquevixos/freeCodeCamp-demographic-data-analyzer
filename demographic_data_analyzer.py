import pandas as pd
import numpy as np


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data')

    # How many people of each race are represented in this dataset? This should be a Pandas series with race names as
    # the index labels. (race column)

    race_count = df['race'].value_counts()

    # What is the average age of men?

    average_age_men = np.mean(([df['age'][i] for i in range(len(df.axes[0])) if df['sex'][i] == 'Male'])).round(
        decimals=1)

    # What is the percentage of people who have a Bachelor's degree?

    percentage_bachelors = round((df['education'].value_counts().get('Bachelors') /
                                  df['education'].value_counts().sum()) * 100, 1)

    # What percentage of people with advanced education (Bachelors, Masters, or Doctorate) make more than 50K?

    higher_education = np.sum(df['education'].value_counts().get(['Bachelors', 'Masters', 'Doctorate']))

    higher_education_salary = len([df['education'][i] for i in range(len(df.axes[0])) if
                                  (df['education'][i] == 'Bachelors' or
                                   df['education'][i] == 'Masters' or
                                   df['education'][i] == 'Doctorate') and
                                   df['salary'][i] == '>50K'])

    higher_education_rich = round((higher_education_salary / higher_education) * 100, 1)


    # What percentage of people without advanced education make more than 50K?

    lower_education = np.sum(df['education'].value_counts()) - higher_education

    lower_education_salary = len([df['education'][i] for i in range(len(df.axes[0])) if
                                  df['salary'][i] == '>50K']) - higher_education_salary

    lower_education_rich = round((lower_education_salary / lower_education) * 100, 1)


    # What is the minimum number of hours a person works per week?

    min_work_hours = df['hours-per-week'].min()


    # What percentage of the people who work the minimum number of hours per week have a salary of more than 50K?

    rich_percentage = (df.loc[(df['hours-per-week'] == 1) &
                              (df['salary'] == '>50K')].value_counts().sum() /
                       len(df.loc[(df['hours-per-week'] == 1)])) * 100


    # What country has the highest percentage of people that earn >50K and what is that percentage?

    country_counts = pd.DataFrame(df.groupby(df['native-country'])['salary'].count()).reset_index()
    country_counts = country_counts.rename(columns={'salary': 'counts'})

    rich_counts = df.loc[df['salary'] == '>50K', ['native-country', 'salary']]
    rich_counts = pd.DataFrame({'rich-counts': rich_counts.value_counts()}).reset_index()

    country_counts = country_counts.merge(rich_counts, on='native-country')
    country_counts['rich-percent'] = round((country_counts['rich-counts'] / country_counts['counts']) * 100, 1)

    top_country = country_counts.sort_values('rich-percent', ascending=False).head(1)

    highest_earning_country = top_country.iloc[0]['native-country']
    highest_earning_country_percentage = top_country.iloc[0]['rich-percent']


    # Identify the most popular occupation for those who earn >50K in India

    india_df = pd.DataFrame([df['occupation'][i] for i in range(len(df.axes[0])) if
                             (df['native-country'][i] == 'India' and df['salary'][i] == '>50K')],
                            columns=['occupation'])

    counts = pd.DataFrame(india_df.value_counts(), columns=['counts'])

    india_df = india_df.drop_duplicates()
    india_df = india_df.merge(counts, on='occupation')

    top_IN_occupation = india_df.iloc[0]['occupation']

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        # print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        # print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
            highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
