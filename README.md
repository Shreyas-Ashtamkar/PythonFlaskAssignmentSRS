# PythonFlaskAssignmentSRS

## **Objective**

The objective of this assignment is to create a feature-rich web application using Python and Flask. The application will allow users to manage and share their favorite recipes. It will include user authentication, database interactions, and dynamic content.

## **Requirements**

### **1\. User Authentication and Authorization**

- Implement user registration and login functionality.
- Use Flask-Login for session management.
- Users should be able to create, edit, and delete their own recipes.

### **2\. Database Schema**

- Choose any relational database (e.g., SQLite, PostgreSQL, MySQL).
- Design a schema to store recipe information:
  - Recipe table with fields:
    - id (integer, primary key)
    - title (string, not null)
    - description (text)
    - ingredients (text or JSON array)
    - instructions (text)
    - created_by (foreign key referencing user)

### **3\. Recipe Management**

- Create CRUD (Create, Read, Update, Delete) endpoints for recipes.
- Allow users to add ingredients (possibly with quantities) to their recipes.
- Implement search functionality to find recipes by title or ingredients.
- Implement pagination for listing recipes.

### **4\. Testing**

- Write unit tests for critical components (e.g., authentication, database interactions).
- Use testing libraries such as pytest or unittest.

## **Submission**

Submit your assignment as a GitHub repository with clear instructions in the README. Include a README.md file with an overview of the project with all endpoints, setup instructions, and any additional notes. Optionally, deploy the application to a cloud platform (e.g., Heroku) and provide the live demo link.

## **Evaluation**

Your assignment will be evaluated based on the following criteria:

- **Functionality**: Does the application meet the specified requirements?
- **Code Quality**: Is the code well-organized, modular, and maintainable?
- **Design Decisions**: How thoughtful are your design choices?
- **Testing**: Are there sufficient tests, and do they cover critical scenarios?
