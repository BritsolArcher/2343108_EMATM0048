# SDPA Project
This project is the course work of `Software Development: Programming and Algorithms (SDPA)`, consisting of `Coffee Shop Simulation` and `Data Analytics`. The project's link is https://github.com/BritsolArcher/2343108_EMATM0048
# Coffee Shop Simulation
## Introduction
This project is a text-based coffee shop simulation programme. In the simulation, the coffee shop needs to have baristas to make the coffee. It also needs to have milk, beans, and spices as ingredients that it purchases from a supplier. Each month the coffee shop owner must decide whether to add/remove baristas, how much coffee to sell for each type, and then pay expenses. The goal of the coffee shop is to make a profit and avoid going bankrupt.
## Functionality
This programme allows users to perform the following operations:
-  Determine the number of months to run the simulation, and the default number is `6`.
-  Choose how many baristas to add/remove.
    - When adding baristas, allow to determine what type of coffee the barista specialises in, but the number of baristas will not exceed `4`.
    - When removing baristas, allow to determine to remove certain baristas, but the coffee shop will keep at least one barista.
-  Determine the monthly demand of each type of coffee, which can not exceed the maximum demand.
## Project Structure
- `/tables`
  - `demand.csv`
  - `ingredients.csv`
  - `pantry.csv`
  - `supplier.csv`
- `barista.py`
- `cash_status.py`
- `coffee_shop.py`
- `data_load.py`
- `main.py`
- `pantry.py`
### Introduction to Classes
#### Base Module:
- `Barista`: The class represents a barista.  
- `BaristaTeam`: The class represents a barista team.  
- `Pantry`: The class represents the pantry of the coffee shop.  
- `CashStatus`: The class represents the cash status of the coffee shop.
#### Core Module:
- `CoffeeShop`: The class represents the coffee shop, regulating the barista team, pantry, and cash status

# Data Analytics
## Introduction
This project is the data analysis of Wikipedia.
## Environment Requirements
To run this script, please ensure the following package has been installed:
- `Wikipedia-API` 0.6.0
- `pandas` 2.0.3
- `numpy` 1.5.0
- `matplotlib` 3.7.2
- `seaborn` 0.12.2
- `scipy` 1.11.1
- `optuna` 3.5.0
- `scikit-learn` 1.2.2
## Project Structure
- `Wikipedia_Data_Analytics.ipynb`
- `rf_classifier.pkl`
- `wiki_data.csv`



