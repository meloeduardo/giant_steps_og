![](https://lh4.googleusercontent.com/JLBbVDeQQY8c6mA3m9Mt-XGha-1b8yj9imwD2pFx5VqW-a7B1R3QctZFSjfOKjs_mOjcynfYMJb3OsGbI1PuLo1kaW1BzCpI8Ztbe5e2yksOveyqS5RgPj1O4ANGVm6azA=w1154)

# Technical Challenge - Internship 2022Q2 - Giant Steps Capital
## 1. The Question.
The question was to find the most profitable interval of 500 days between  2000-01-01 until 2022-03-31 to invest in the SELIC interest rate.

Here's how I did it.

![](https://imgur.com/WiIGaRz.gif)

### The first step, get the data.

I used the requests library to get the JSON data structure from the BCB API provided.

```python
import requests
import pandas as pd
def get_json(dataInicial='dd/mm/yy', dataFinal='dd/mm/yy'):
    payload = {'formato': 'json',
               'dataInicial': dataInicial,
               'dataFinal': dataFinal}
    api_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados'
    response = requests.get(api_url, params=payload)
    return response.json()
```
The code above returns thousands of lines like the one below.
It is a list of dictionaries.
![](https://imgur.com/LWuj2A8.jpg)

### Now that I have the data, the fun begins.
First of all, I built a function to handle this data and return what I want. The daily, monthly, and yearly earned amount on a specific value. 
I built a function to find it, I am going to explain the steps.

#### Explaining the function, step one: validation of function arguments.
```python
def hist_data(start_date, end_date, capital, frequency):
    assert capital > 0, "Capital arg must be greater than 0"
    assert frequency in ['day', 'month','year'], "frequency arg must be day, month or year."
    assert pd.to_datetime(start_date) > pd.to_datetime('1995-01-01'), "start_date must greater than 1995-01-01"
    assert (pd.to_datetime(start_date) > pd.to_datetime(end_date)) is False, "start_date arg must be greater than end_date arg"
```
##### capital <= 0 and the error.
```python
hist_data('2010-01-01', '2021-03-01', 0, 'day')
```
![](https://imgur.com/vM7nvLQ.jpg)
##### not using the correct frequency.
```python
hist_data('2010-01-01', '2021-03-01', 100, 'not_a_day')
```
![](https://imgur.com/hvpkGOv.jpg)
##### start_date not greater than 1995-01-01.
```python
hist_data('1995-01-01', '2021-03-01', 100, 'day')

```
![](https://imgur.com/B9Y2QgZ.jpg)
##### start_date greater than end_date.
```python
hist_data('2005-01-01', '2002-01-01', 100, 'day')
```

![](https://imgur.com/Ro00FqI.jpg)

### Step two: the pandas library and building the ideal dataframe.

I chose the pandas library for the ease of manipulating the data, making the code more concise.

```python
    df = pd.DataFrame(get_json())
    df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y")
    df['valor'] = pd.to_numeric(df['valor'])
    df = df[(df['data'] >= start_date) & (df['data'] <= end_date)]
    df.reset_index(drop=True, inplace=True)
    df.loc[0, 'capital'] = capital
```
What does the code above do?
1. Transforms the list of dictionaries into a data structure called DataFrame.
2. Converts the data type to make manipulation more precise, concise, and easier.
3. Leaves only the date scope that is passed in the argument
4. Reset the index, the index of first row is now 0.

### Step three:  Creating new column.

```python
for i in range(len(df)):
        df.loc[i, 'Amount earned'] = df.loc[i,'capital'] - [0, 'capital']
        df.loc[i+1, 'capital'] = df.loc[i, 'capital'] + \ (df.loc[i, 'valor'] * df.['capital /100)
df.dropna(inplace=True)
```
In the loop above there is just one function: Create the  `Amount earned` and `capital` columns. It loops through the dataframe and updates the data based on the previous row.

little observation, my first thought was to use the NumPy vectorization for better performance than just loops, but it wasn't possible, I needed to know the first row data first.


### Step four:  The heart of the function.
```python
if(frequency == 'day'):
    pass
if(frequency == 'month'):
    df = df.loc[df.groupby(pd.Grouper(key='data', freq='1M')).data.idxmax()]
if(frequency == 'year'):
    df = df.loc[df.groupby(pd.Grouper(key='data', freq='1Y')).data.idxmax()]
df.rename(columns={'data': 'Date', 'capital': 'Capital'}, inplace=True)
df = df.drop(columns=['valor'])
return df
```
Ok, the `day` interval is the default, look below.
```python
hist_data('2010-01-01', '2021-03-01', 657.43, 'day')
```
![](https://imgur.com/7HG3t1N.jpg)

There is no work to be done here, the next step is the monthly and yearly dataframe.

The one line below will filter the last days of the months by grouping by `Date` with `pd.Grouper` set to one month, then getting the last row from each group:
```python
df = df.loc[df.groupby(pd.Grouper(key='data', freq='1M').data.idxmax()]
```
The same line works for `years`, just changing the freq argument to 1Y.

```python
hist_data('2010-01-01', '2021-03-01', 657.43, 'month')
```

![](https://imgur.com/pkLPNp9.jpg)

```python
hist_data('2010-01-01', '2021-03-01', 657.43, 'year')
```

![](https://imgur.com/rbKY1lc.jpg)

This is enough, now let's create the function that answers the question.

### The question answer.
Straight to the point.
<b>2002-07-08 until 2003-11-20</b> was the most profitable interval of 500 days between 2000-01-01 until 2022-03-31 to invest in the SELIC interest rate. 

32.387964% percent appreciation in 500 days.

```python
def most_profitable_period(start_date, end_date):
    """use example: most_profitable_period('01-01-2000', '31-03-2022')."""
    df = hist_data(start_date, end_date, 100, 'day')
    df.set_index('Date', inplace=True)
    df.index.names = ['end_date']
    df['%.increase'] = df['Capital'].pct_change(periods=500, freq='D')
    df.sort_values(by='%.increase', ascending=False, inplace=True)
    df['start'] = df.index - pd.to_timedelta(500, unit='d')
    df.drop(columns=['Amount earned', 'Capital'], inplace=True)
    df.dropna(inplace=True)
    return df
```
The thought process here is simple: just get the most profitable interval(biggest positive percentual change) in the 500 days interval.

