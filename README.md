# E-commerce Backend API

This is a fast and scalable backend solution for e-commerce platforms, built using Python and FastAPI. It provides essential features like user authentication, product management, cart handling, and order processing.

## Features

- **User Authentication**: Register, login,  authentication.
- **Product Management**: CRUD operations for products and categories.
- **Cart and Orders**: APIs to add items to cart and place orders.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- MongoDB(NoSql) (Database of choice)
- Pydantic (for data validation)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Uditdev21/ecomm-backend.git
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables (e.g., database credentials, secret keys).

4. Run the application:
    ```bash
    uvicorn main:app --reload
    ```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to open issues or submit pull requests. Contributions are welcome!

## .env

the dot env file containes
```
DBSTRING="database connection string"
CLOUDINARY_API_SECRET="cloudinary api secret"
CLOUDINARY_API_KEY="cloudinary api key"
CLOUDINARY_CLOUD_NAME="cloudinary cloud name"
```
test run