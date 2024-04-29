# Vendor Management System

## Overview
The Vendor Management System is a Django-based web application designed to manage vendor profiles, track purchase orders, and evaluate vendor performance metrics. This system provides a comprehensive solution for businesses to streamline their vendor management processes efficiently.

## Features
- **Vendor Profile Management:** Create, update, delete, and list vendor profiles with essential information such as name, contact details, and address.
- **Purchase Order Tracking:** Track purchase orders including order details, status, and vendor references.
- **Vendor Performance Evaluation:** Calculate and display vendor performance metrics including on-time delivery rate, quality rating average, average response time, and fulfillment rate.

## Setup Instructions
1. **Clone the Repository:**
   ```
   git clone <repository-url>
   cd vendor_management
   ```

2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Apply Migrations:**
   ```
   python manage.py migrate
   ```

4. **Create a Superuser:**
   ```
   python manage.py createsuperuser
   ```

5. **Run the Development Server:**
   ```
   python manage.py runserver
   ```

6. **Access the Admin Interface:**
   Open a web browser and go to `http://127.0.0.1:8000/admin` to access the admin interface. Log in with the superuser credentials created earlier.

7. **API Endpoints:**
   - Vendor Profile Management:
     - `POST /api/v1/vendors/`: Create a new vendor.
     - `GET /api/v1/vendors/`: List all vendors.
     - `GET /api/v1/vendors/<vendor_id>/`: Retrieve a specific vendor's details.
     - `PUT /api/v1/vendors/<vendor_id>/`: Update a vendor's details.
     - `DELETE /api/v1/vendors/<vendor_id>/`: Delete a vendor.

   - Purchase Order Tracking:
     - `POST /api/v1/purchase_orders/`: Create a purchase order.
     - `GET /api/v1/purchase_orders/`: List all purchase orders with an option to filter by vendor.
     - `GET /api/v1/purchase_orders/<po_id>/`: Retrieve details of a specific purchase order.
     - `PUT /api/v1/purchase_orders/<po_id>/`: Update a purchase order.
     - `DELETE /api/v1/purchase_orders/<po_id>/`: Delete a purchase order.

   - Vendor Performance Evaluation:
     - `GET /api/v1/vendors/<vendor_id>/performance/`: Retrieve a vendor's performance metrics.

## Logic Overview
- **Vendor Performance Evaluation:**
  - On-Time Delivery Rate: Calculated each time a PO status changes to 'completed'.
  - Quality Rating Average: Updated upon the completion of each PO where a quality_rating is provided.
  - Average Response Time: Calculated each time a PO is acknowledged by the vendor.
  - Fulfillment Rate: Calculated upon any change in PO status.

## Technologies Used
- Django
- Django REST Framework
- SQLite

