# your financier
Telegram bot to manage budgets with monobank integration. 


## Features
- manage budget-based spendings
- view leftover to the end of day or period
- categories support
- integration with [monobank](https://api.monobank.ua/docs/) to add spendings by credit card automatically
- group budgets support


## Stack
- Python
- Aiogram
- Redis
- MongoDB
- fastAPI
- Docker


## Demo
https://youtu.be/lsmeZ-hASbg


## Bugs
- [ ] when adding transaction to _personal_, it search by name and adds to the first found budget by mistake


## Improvements
- [ ] handle multiple budgets with the same name
- [ ] handle groups with the same name
- [ ] hide feature to view budget transactions if there is no transactions
- [ ] sort transactions by date?
- [ ] handle many transactions in budget, when user wants to view them
- [ ] show only transactions of selected budget, not all at once
- [ ] show invitation text when user joined by invite link
- [ ] when user opened invite link, show that group is added (to all users?)
- [ ] do not suggest select group if only _personal_ is created
- [ ] message about transaction added successfully
- [ ] hide _spender_ if transaction was in _personal_ group
- [ ] handle bad user input
- [ ] security — hash in db, do not use group and member id in url
- [ ] add logging
- [ ] open access to all users, not admin only
- [ ] move environment variables to .env, create .env-example
- [ ] dockerize app


## Features
- [ ] move transaction to another budget
- [ ] notify about ending or overusing of budget (to the end of day or period)
- [ ] beautify interfaces
- [ ] add transaction to all/multiple budgets
- [ ] implement `rollback`

