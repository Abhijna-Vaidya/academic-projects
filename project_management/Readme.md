# Collaborative Student Project Monitoring and Management Tool 
A web-based platform designed to streamline project management for students, enabling seamless 
collaboration, progress tracking, and role-based access for students, guides, and coordinators. It simplifies 
group formation, project submissions, and performance evaluation. 

## Procedure to Run the Project-Management Web App

1. **Create a Superuser**
   
   Run the following command to create an admin account:
   ```bash
   python manage.py createsuperuser
   ```

2. **Start the Development Server**

    ```bash
    python manage.py runserver
    ```

3. **Login as Admin**

    ```bash
    http://127.0.0.1:8000/admin
    ```

4.  **Upload CSV Files**

After logging in as admin:

- Upload CSV files containing student and teacher information  
- Ensure the CSV files follow the same format as provided in the `sample_csv_files/` folder


### Push Notifications Setup

#### Install Required Python Packages
```bash
npm install -g web-push
pip install pywebpush cryptography
```
#### Generate VAPID Keys
```bash
npx web-push generate-vapid-keys
```