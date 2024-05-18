import click
import json
import logging


logging.basicConfig(
    filename='app.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('expense')

@click.group()
def cli():
    """
    The Expense CLI tool.
    """
    pass


def get_friend_names(num_friends):
    """
    Get names of friends in a new expense session.
    """
    friends = {}
    for i in range(num_friends):
        name = click.prompt(f"Friend {i+1} name")
        friends[name] = None
    return friends

def get_expenses(name):
    """
    Get expenses incurred by a friend in a new expense session.
    """
    expenses = []
    while True:
        expense_name = click.prompt(f"Expense incurred by {name}", default="", type=str)
        logger.info(f"Expense incurred by {name}: {expense_name}")
        if not expense_name:
            return expenses
        expense_amount = click.prompt(f"Amount of {expense_name}", type=float)
        logger.info(f"Amount of {expense_name}: {expense_amount}")
        expenses.append({'name': expense_name, 'amount': expense_amount})

@cli.command()
@click.argument('num_friends', type=int)
def start_session(num_friends):
    """
    Start a new expense session.
    """
    friends = get_friend_names(num_friends)
    for name in friends:
        friends[name] = {'expenses': get_expenses(name)}
        logger.info(f"Expenses incurred by {name}: {friends[name]['expenses']}")
    with open('expenses.json', 'w') as file:
        json.dump(friends, file)


@cli.command()
def calculate_expenses():
    with open('expenses.json') as file:
        friends = json.load(file)
    total = sum(expense['amount'] for friend in friends.values() for expense in friend['expenses'])
    print(f"Overall total: {total}")
    total_expenses = sum(expense['amount'] for friend in friends.values() for expense in friend['expenses'])
    num_friends = len(friends)
    average_expenses = total_expenses / num_friends
    print(f"Average expenses: {average_expenses}")
    for friend in friends:
        friend_expenses = sum(expense['amount'] for expense in friends[friend]['expenses'])
        logger.info(f"Expenses incurred by {friend}: {friend_expenses}")
        difference = average_expenses - friend_expenses
        if difference > 0:
            print(f"{friend} owes {difference} to {next(filter(lambda f: f != friend, friends))}")
        elif difference < 0:
            print(f"{next(filter(lambda f: f != friend, friends))} owes {-difference} to {friend}")
        else:
            print(f"{friend} and {next(filter(lambda f: f != friend, friends))} have same expenses")
        # Update the difference for the next friend
        average_expenses += difference

@cli.command()
def print_expenses():
    """
    Print the json data stored in the file.
    """
    with open('expenses.json') as file:
        data = json.load(file)
    print(json.dumps(data, indent=4))

if __name__ == '__main__':
    cli()

