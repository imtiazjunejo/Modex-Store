# Flask Application Architecture for Modex Store

## Overview
This document outlines the architecture for converting the static Modex Store website into a dynamic Flask web application. The application will feature user authentication, database-driven product management, and server-side cart functionality.

## Project Structure
```
modex_store/
├── app.py                 # Main Flask application
├── models.py             # SQLAlchemy database models
├── routes.py             # Route definitions
├── config.py             # Application configuration
├── requirements.txt      # Python dependencies
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template with navbar/footer
│   ├── index.html        # Home page
│   ├── shop.html         # Shop page
│   ├── cart.html         # Cart page
│   ├── login.html        # Login page
│   └── signup.html       # Signup page
└── static/               # Static files
    ├── css/
    │   └── style.css     # Main stylesheet
    ├── js/
    │   ├── main.js       # Cart and UI functionality
    │   └── products.js   # Product-related JS (modified)
    └── images/           # Product images
        ├── hoodie.jpg
        ├── tshirt.jpg
        └── ...
```

## Routes
- `GET /` - Home page with hero section and featured products
- `GET /shop` - Shop page displaying all products
- `GET /cart` - Cart page (requires authentication)
- `GET/POST /login` - User login
- `GET/POST /signup` - User registration
- `GET /logout` - User logout
- `POST /add_to_cart/<product_id>` - Add product to cart
- `POST /remove_from_cart/<product_id>` - Remove product from cart

## Database Schema

### User Model
```python
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)
```

### Product Model
```python
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
```

### CartItem Model
```python
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
```

## Template Integration
- Convert existing HTML files to Jinja2 templates
- Create `base.html` with common navbar and footer
- Use template inheritance: `{% extends 'base.html' %}`
- Dynamic product rendering using `{% for product in products %}`
- Static file references: `{{ url_for('static', filename='css/style.css') }}`

## Authentication & Session Management
- Use Flask-Login for session management
- Password hashing with Werkzeug
- Login required decorator for cart and checkout routes
- Cart persistence in database for authenticated users
- Local storage fallback for anonymous users

## Cart Functionality
- Server-side cart storage for logged-in users
- AJAX calls for add/remove cart items
- Cart count display in navbar
- Cart total calculation
- Clear cart functionality

## Key Technologies
- Flask: Web framework
- SQLAlchemy: ORM for database operations
- Flask-Login: User session management
- Jinja2: Template engine
- Werkzeug: Password hashing
- SQLite/PostgreSQL: Database (configurable)

## Security Considerations
- CSRF protection on forms
- Password hashing
- Session management
- Input validation
- SQL injection prevention via ORM

## Deployment Considerations
- Environment variables for configuration
- Database migrations with Flask-Migrate
- Static file serving in production
- Session secret key management