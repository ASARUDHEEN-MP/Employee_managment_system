# Employee Management System

## Overview
This project is an Employee Management System that allows admin and employee to sign up, manage employees, and dynamically handle employee fields by admin . The system features a user-friendly interface for managing employee data and includes robust search and filter functionality.

### Technologies Used
- **Database**: PostgreSQL for data storage.
- **Testing**: Django's  framework for API .

### Employee Support
The system supports multiple Employee, ensuring that:
- Each Employee can login,signup,.
- Changes made to Profile fields 
- Employees can add profilepic,update profile ,changepassword.

### Admin
The system supports Admin to create fields to employee and create position that can choose by employee:
- Each employees can choose position that added by admin .
- admin manage employee fields also delete .
- admin get listed Employee and block if needed.

## Features
- **User Authentication**: login page for Employee in same page admin .
- **Dashboard**: A simple dashboard for navigating the employee module.
- **Employee Module**:
  - View a list of employees with search capability.
- **Dynamic Field Management**: Manage employee fields, allowing admin to add and modify fields dynamically.

## Installation

### Prerequisites
- Python 3.x
- Django
- PostgreSQL


### Steps


### Clone the Repository and Set Up the Environment
Follow these steps to clone the repository and set up the virtual environment:

1. Clone the repository:
    ```bash
    git clone [https://github.com/ASARUDHEEN-MP/Employee_managment.git](https://github.com/ASARUDHEEN-MP/Employee_managment_system)
    ```


2. Create a virtual environment:
    ```bash
    python -m venv venv


    ```

3. Activate the virtual environment:
    - For macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    - For Windows:
        ```bash
        venv\Scripts\activate
        ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Create a .env File
Create a `.env` file in the project directory to store your database configuration. Use the following template:

```plaintext
# Database settings
DB_NAME='your_database_name'
DB_USER='postgres'
DB_PASSWORD='your_password'
DB_HOST='localhost'
DB_PORT=5432
```
6.Run Migrations
```bash
    python3 manage.py migrate

```
7.create super user
```bash
    python3 manage.py createsuperuser

```

8.Start the Server
```bash
    python3 manage.py runserver
```
You can now access the API at http://127.0.0.1:8000/
http://127.0.0.1:8000/api/** This for Employee side
http://127.0.0.1:8000/api/admin/*** This for Admin side


9.Testing
```bash
    python manage.py test employees
```
## API Endpoints

### 1. User Registration
- **URL**: `http://127.0.0.1:8000/api/register/`
- **Method**: `POST`
- **Request Body**: 
    ```json
     {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "password": "yourpassword"
  }

    ```
- **Response**: 
    - On successful registration:
        ```json
        {
            "message": "User registration is successful..."
        }
        ```
    - On error (e.g., validation errors):
        ```json
        {
            "errors": {
                "email": ["This field is required."],
                "name": ["This field is required."],
                "password": ["This field is required."]
            }
        }
        ```
### 2. User Login
- **URL**: `http://127.0.0.1:8000/api/login/`
- **Method**: `POST`
- **Request Body**: 
    ```json
       {
      "email": "johndoe@example.com",
      "password": "yourpassword"
    }
    ```
- **Response**: 
    - On successful login:
        ```json
        {
          "user_id": 14,
          "token": {
              "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMDY2MTM2MSwiaWF0IjoxNzMwNTc0OTYxLCJqdGkiOiIzZDBlOTk0ZWUyMmE0ODYxOTFlNmM2ZTQzZWQwNjllNCIsInVzZXJfaWQiOjE0fQ.QX4BGArlAnoGQozKWEhJWNXgA9vYrT8TEU7fp0RSRIU",
              "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwODM0MTYxLCJpYXQiOjE3MzA1NzQ5NjEsImp0aSI6IjljYzhjNDQzODZhZTRhNGNiNGQxYjk5MWNhYmE1NWUxIiwidXNlcl9pZCI6MTR9.vd_hgete1fYu4P7sK71VsYAl-dfQMJ8-nfQJAZCX3Nw"
          },
          "user_role": "Employee",
          "message": "Successfully logged in"
      }
        ```
    - On error (e.g., validation errors if password or username is null):
        ```json
        {
            "errors": {
                "name": ["This field is required."],
                "password": ["This field is required."]
            }
        }
        ```
        Or for invalid credentials:
        ```json
        {
            "errors": {
                "non_field_errors": [
                    "Invalid password."
                ]
            }
        }
        ```
        Or:
        ```json
        {
            "errors": {
                "non_field_errors": [
                    "Invalid email."
                ]
            }
        }
        ```

**reqyest for access token when the access token expiery with valid refresh token**

- **URL**: `http://127.0.0.1:8000/api/token/refresh/`
- **Method**: `POST` 
- **Request Body**:
 - **Response**: 
    - On successful login:
        ```
              {
          "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwODc3NDA0LCJpYXQiOjE3MzA2MTgxNjYsImp0aSI6ImYyYTU5YmJlMTRiYjRjNmZhMDQ1OWZjMjJiYWZmYjAwIiwidXNlcl9pZCI6MTV9.MXYlHWxSJyRWQ4zGoCrQbcpyBIygGuJjtLfpHhsKsoQ",
          "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMDcwNDYwNCwiaWF0IjoxNzMwNjE4MjA0LCJqdGkiOiI0NjU1MDdkOWIyYzA0MmQyYTAzZThkMzg4NDdlNTJiOSIsInVzZXJfaWQiOjE1fQ.xtR-7wZP6XVCS36AQ2-SOG4LaFyQs5npGp-Lmx7XZhE"
      }
        ```
**Update Employee Whwn regutser automatically the profile will create by signals**

- **URL**: `http://127.0.0.1:8000/api/Employee/`
- **Method**: `PUT` 
- **Request Body**:
  ```json
  {
    "id": 13,
    "name": "test",
    "email": "test1@gmail.com",
    "employeeprofile": {
        "profile_image": null,
        "position": 5
    },
    "custom_fields": [
        {
            "custom_field": 4,  // Replace with the actual primary key of the CustomField
            "value": "5"
        }
    ]
   }

  ```
- **Response**: 
    - On successful :
        ```json
                             [
                    {
                        "id": 14,
                        "name": "test1",
                        "email": "test1@gmail.com",
                        "employeeprofile": {
                            "id": 9,
                            "position": 3,
                            "position_title": "Managers"
                        },
                        "custom_fields": [
                            {
                                "custom_field_id": 4,
                                "field_name": "phonenumber",
                                "field_type": "number",
                                "value": "702593282"
                            },
                            {
                                "custom_field_id": 5,
                                "field_name": "address",
                                "field_type": "text",
                                "value": ""
                            }
                        ]
                    }
                ]
        ```
    - On error (e.g., validation errors if password or username is null):
        ```json
       
        ```
        Or for invalid credentials:
        ```json
               {
        "error": "This field is required."
      }

        ```
        Or:
        ```json
        {
        "error": "An unexpected error occurred."
      }

        ```

### 5. Search Employees

**Search Employees**

- **URL**: `http://127.0.0.1:8000/api/employees/?data`
- **Method**: `GET`
- **Query Parameters**:
  - `search`: (optional) A string to search for in employee names, emails, or phone numbers.("http://127.0.0.1:8000/employee/api/employees/?search=manu@g")

**Responses**
- **200 OK:**
  - **Description**: Returns a list of employees matching the search criteria.
  - **Example**:
  ```json
  [
    {
      "id": 2,
      "user": 1,
      "name": "Alice Johnson",
      "email": "alice.johnson@example.com",
      
    }
  ]


#### Create Postion

- **URL**: `http://127.0.0.1:8000/api/admin/positions/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "title": "Custom Field Name",
  
  }

**Responses**
- **200 OK:**
  - **Description**: Custom field created successfully..
  - **Example**:
  ```json
       {
    "id": 1,
    "user": 1,
    "field_name": "Custom Field Name",
      "field_type": "text"
    }

- **400 OK:**
  - **Description**: Custom field created successfully..
  - **Example**:
  ```json
     {
      "error": "A custom field with this name already exists for this user."
    }




  
**List Employee To Admin**

- **URL**: `http://127.0.0.1:8000/api/admin/Employees/`
  - **Method**: `get`
- **Request Body**:
  ```json
 
- **Response**: 
    - On successful login:
        ```json
       [
          {
              "id": 14,
              "name": "test1",
              "email": "test1@gmail.com",
              "is_active": true,
              "profile": {
                  "user": 14,
                  "profile_image": "http://127.0.0.1:8000/media/profile_images/Screenshot_2024-09-25_at_1.25.56PM.png",
                  "position": {
                      "id": 3,
                      "title": "Managers"
                  }
              }
          }
      ]
  ```
- **400 Bad Request**:
  ```json
       {
        "error": "Invalid custom field: \"name of that field\""
      }
  ```

  ** CREATE GET custom_fields THIS WANT TO USE BY CONNECT TO THE Employee fields so if we need to connect to other table we can add to other Employee**

- **URL**: `http://127.0.0.1:8000/api/admin/custom_fields/`
  - **Method**: `get,post,put`
- **Request Body**:
  ```json
  {
          "field_name":"blaaa",
          "field_type":"Number,text"
          }

 
- **Response**: 
    - On successful login:
        ```json
       {
        "field_name":"blaaa",
        "field_type":"Number,text"
        }
  ```
- **400 Bad Request**:
  ```json
       {
        "error": "if there is the same field_name will back the error and admin can allow to create ""
      }
  ```



   ** CREATE GET custom_fields_value connect the custom_fields with Employee with user custom_fields from custom_fields table value can be added by Employee**

- **URL**: `http://127.0.0.1:8000/api/admin/custom_fields_value/`
  - **Method**: `get,post,put,delete`
- **Request Body**:
  ```json
     {
            "user": 13,
            "custom_field": 5,
            "value": ""
            
        }
 
- **Response**: 
    - On successful login:
        ```json
            {
          "user": 13,
          "custom_field": 5,
          "value": ""
          
      }

  ```
- **400 Bad Request**:
  ```json
       {
        "error": "if Employee is the same field_name will back the error and admin can allow to create ""
      }
  ```
  

  

