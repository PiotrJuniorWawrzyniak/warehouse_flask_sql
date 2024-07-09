# Warehouse Management System

## Description

The Warehouse Management System is a web application that allows for managing warehouse inventory, tracking the history of operations, and updating account balance. The application is built using the Flask framework and SQLite for the database.

## Features

- **Add Products to Warehouse**: Ability to add new products along with their price and quantity.
- **Sell Products**: Sell existing products from the warehouse.
- **Update Balance**: Update the account balance.
- **Operation History**: Track all operations performed on the warehouse with the ability to filter the range of operations.
- **Data Validation**: Check the correctness of entered data both in forms and through the URL.

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd warehouse_flask_sql
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

## Usage

### Adding Products

1. Go to the main page of the application.
2. Fill out the "Purchase" form by providing the product name, price, and quantity.
3. Click the "Buy" button.

### Selling Products

1. Go to the main page of the application.
2. Fill out the "Sell" form by providing the product name and quantity.
3. Click the "Sell" button.

### Updating Balance

1. Go to the main page of the application.
2. Fill out the "Update Balance" form by providing the amount to add/subtract.
3. Click the "Update Balance" button.

### Operation History

- To display all operations, go to the [Operation History](http://127.0.0.1:5000/historia) page.
- To display operations in a specific range, enter the range in the form on the "Operation History" page or use the URL format: `http://127.0.0.1:5000/historia/<from>/<to>`. If an invalid range is provided, an appropriate message will be displayed.

## Authors

- Piotr Wawrzyniak

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
