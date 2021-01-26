# Analytical task for INT20H 2020

**Xterm-inate** team

---

## Task Description

Create a console application for calculating LTV of input data.

**User interaction flow** is the following:

0. Trial
1. First purchase
2. Second purchase
3. N-th purchase

User makes weekly subscriptions which can be cancelled at any point. 

Apple store takes **30% fee** from each purchase in the application.

Application **price** is $9.99.

## Task Solution

First of all, taking into account user interaction flow, we will have (N - 1) "rolling" (kinda) retention values: from trial to first purchase, from first purchase to second purchase and so on.

From the initial data, we will only need  2 columns:`Subscriber ID` and `Event Date`. We can drop all other columns \`cause in the provided dataset, all other columns are not needed for this task.

We can calculate LTV using given data through 2 different approaches:

1. Using retention.
2. Using average lifetime money spent (the method is taken from [here](https://www.thebalancesmb.com/how-to-calculate-the-lifetime-value-of-a-customer-4173824)).

For both methods, we will need an array of users renewing the subscription for each week (from 0-'trial' to N-1) and for the second method, we will additionally use an array of weeks from 0 to N-1.

To get this data we simply need to do some pandas grouping and aggregation.

The first grouping is done by `Subscriber ID` with `count` aggregation. This will tell us how many weeks each individual user was interested in buying our application.

The second grouping is done by `Event Date` with `count` aggregation. This will give us information about how many users bought our application every week.

Using these two groupings we will have a dataset where the index is the week number and a single column represents users who renewed their subscription after week 1.

<details><summary>Code for this operation</summary>

Thank you for opening this spoiler. I thought it will never be opened. Groupings stuff is here.

```python
data = (data
        .groupby(by="Subscriber ID").count()
        .reset_index()
        .groupby(by="Event Date").count()
        .sort_index()
        )["Subscriber ID"]
weeks, user_counts = data.index.values - 1, data.values
```

</details>

### Using Retention

We should mention that (just for now) we did not take into account users week-N users into the week-(N-1)...week-0 users, so we must fix it.

First of all, we revert the user's array so that we have users in order week-N to week-0, and take the cumulative sum. That trick will sum users from week-N to users from the week-(N-1), week-(N-2) and so on. Now we only need to revert the list backwards.

<details><summary>Code for this operation</summary>

Hey, you are back! Nice to meet you... Again. We are counting users by weeks here, come to see it.

```python
users = user_counts[::-1].cumsum()[::-1]
```

</details>

To calculate rolling retention we should divide users from week-N to week-(N-1). To do that we just shift our list to left and divide it by its original.

<details><summary>Code for this operation</summary>

Wow, you opened it. Very impressive. Just simple shift and division code here. ~~Why I have created a spoiler for it?~~

```python
users[1:] / users[0:-1]
```

</details>

Next part is just cumulative production of all the elements in the list and its multiplication by `price * (1 - fee)`.

### Using Average Lifetime Money Spent

This is quite easy. We do not have users who pay in week-0, so we just multiply week numbers by the number of users who paid and multiply it by `price * (1 - fee)`. We will get the distribution of money spent by users depending on how long do they use our app. The next step is just sum and division by the number of users.

## Application Usage

The first of all to start using it you must install Python 3. You can find it [here](https://www.python.org/downloads/).

The next step is installing additional libraries to use this app. This can be done running next command from command line ~~(hope you are using Linux, omg)~~.

```bash
pip install -r requirements.txt
```

And only now we got to the step where you use our app.

To get help how to run it you can use:

```bash
python ltv.py -h
```

This will give you all parameters description and show an example on how to run it.

To run the program with default parameters:

```bash
python ltv.py
```

The full application command is next(all parameters are optional):

```bash
python --path PATH/TO/FILE --price 10 --fee 0.1 --with-retention
```

To change the path to file with data use `--path PATH/TO/FILE` parameter.

To change application price use `--price` parameter.

To change market fee `--fee` parameter.

To run the application with retention calculations use `--use-retention` parameter.

## Timing

This stuff is freaking fast. Just look at it!

![Here must be all the time stuff but it is lost. Come back later, please.](./static/timing.png)

## Team Xterm-inate

- Vladyslav Zalevskyi (Tg: @vzalevskyi)
- Vladyslav Rudenko (Tg: @VVRud)
- Olga Pashneva (Tg: @DDR335)
- Olena Radchykova (Tg: @oradchykova)

![Bye bye!](https://media.giphy.com/media/1xucXbDnMIYkU/giphy.gif)
