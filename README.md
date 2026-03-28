# Butchery Management System

A comprehensive Django-based web application for managing a butchery business, featuring both customer-facing e-commerce functionality and staff administrative tools.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Features

### Customer Features
- **Product Catalog**: Browse premium meat products with detailed descriptions and images
- **Shopping Cart**: Add products to cart with quantity management
- **User Authentication**: Secure registration and login system with custom validation
- **Order Management**: Place orders and view order history
- **Responsive Design**: Mobile-friendly interface with modern UI/UX
- **Landing Page**: Attractive hero section with featured products

### Staff/Admin Features
- **Dashboard**: Comprehensive analytics with key metrics and statistics
- **Product Management**: CRUD operations for products with image upload
- **Order Management**: View and manage customer orders with status tracking
- **Sales Analytics**: Daily sales charts and revenue tracking
- **Export Functionality**: Export product data in multiple formats (CSV, PDF, Excel, ODT)
- **Category Management**: Organize products by categories
- **User Management**: Monitor customer accounts and activity

### Technical Features
- **AJAX Integration**: Dynamic cart updates without page refresh
- **Session-based Cart**: Cart persistence across sessions
- **Image Handling**: Product image upload and management
- **Search & Filtering**: Advanced product search and filtering options
- **Pagination**: Efficient data pagination for large datasets
- **Error Handling**: Comprehensive error handling and user feedback
- **Dark Mode Support**: Theme switching capability

## 🛠 Tech Stack

- **Backend**: Django 4.2.20
- **Database**: SQLite (development)
- **Frontend**: HTML5, CSS3, JavaScript, TailwindCSS
- **Icons**: Font Awesome
- **Media Handling**: Django ImageField with PIL
- **Authentication**: Django's built-in authentication system

## 📁 Project Structure

```
butchery/
├── accounts/                 # User account management
│   ├── templates/
│   ├── views.py
│   └── urls.py
├── dashboard/               # Admin dashboard
│   ├── templates/
│   ├── views.py
│   ├── forms.py
│   ├── utils.py
│   └── urls.py
├── shop/                    # E-commerce functionality
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── butchery/               # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                  # User uploaded files
├── manage.py
└── db.sqlite3
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd butchery
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   # For export functionality, also install:
   pip install openpyxl reportlab odfpy
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser account**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python manage.py shell
   # In Django shell, create sample categories and products
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Customer interface: http://127.0.0.1:8000/
   - Admin dashboard: http://127.0.0.1:8000/dashboard/
   - Django admin: http://127.0.0.1:8000/admin/

## 📱 Usage

### For Customers

1. **Browse Products**: Visit the homepage to see featured products
2. **Product Details**: Click on any product to view detailed information
3. **Add to Cart**: Add desired quantities to your shopping cart
4. **Register/Login**: Create an account or login to place orders
5. **Checkout**: Review cart and place orders
6. **Order History**: View your past orders and their status

### For Staff/Administrators

1. **Dashboard Access**: Login with staff credentials to access admin dashboard
2. **Product Management**: 
   - Add new products with images and descriptions
   - Edit existing product information
   - Manage product availability
3. **Order Management**: 
   - View all customer orders
   - Update order status (pending/delivered)
   - Filter orders by status
4. **Analytics**: 
   - Monitor sales performance
   - View revenue trends
   - Track popular products
5. **Export Data**: Export product information in various formats

## 🔌 API Endpoints

### Customer Endpoints
- `GET /` - Landing page
- `GET /products/` - Product listing
- `GET /products/<id>/` - Product details
- `POST /cart/add/<id>/` - Add to cart
- `GET /cart/` - View cart
- `POST /checkout/` - Place order
- `GET /orders/` - Order history

### Dashboard Endpoints
- `GET /dashboard/` - Dashboard home
- `GET /dashboard/products/` - Product management
- `GET /dashboard/orders/` - Order management
- `GET /dashboard/analytics/` - Sales analytics
- `POST /dashboard/products/create/` - Create product
- `PUT /dashboard/products/<id>/` - Update product
- `DELETE /dashboard/products/<id>/` - Delete product

### API Data Endpoints
- `GET /dashboard/api/stats/` - Dashboard statistics (JSON)
- `POST /cart/update/<id>/` - Update cart quantity (AJAX)
- `GET /cart/count/` - Get cart count (AJAX)

## 🎨 Screenshots

*(Add screenshots of your application here)*

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Media Files

Product images are stored in the `media/product_images/` directory. Make sure this directory has proper write permissions.

### Database

The application uses SQLite by default. For production, consider using PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'butchery_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

## 📊 Models

### Product Model
- `name`: Product name
- `description`: Product description
- `price`: Product price (Decimal)
- `category`: Foreign key to Category
- `available`: Availability status
- `image`: Product image (optional)

### Order Model
- `user`: Foreign key to User
- `product`: Foreign key to Product
- `quantity`: Order quantity
- `created_at`: Order date
- `is_delivered`: Delivery status

### Category Model
- `name`: Category name

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 📞 Support

For support and questions, please contact [jackomolo168@example.com] or create an issue in the GitHub repository.

---

**Medaeves Butchery Management System** - Premium meat products with comprehensive business management tools.
