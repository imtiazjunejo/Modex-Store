from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from config import Config
from models import db, User, Product, CartItem, Order, OrderItem
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_categories():
    try:
        categories = db.session.query(Product.category.distinct()).all()
        categories = [c[0] for c in categories if c[0]]
    except:
        categories = []
    return dict(all_categories=categories)

@app.route('/')
def index():
    products = Product.query.all()
    categories = db.session.query(Product.category.distinct()).all()
    categories = [c[0] for c in categories if c[0]]
    # Filter out pants and accessories from homepage
    excluded_categories = ['pants', 'accessories']
    categories = [cat for cat in categories if cat.lower() not in [ex.lower() for ex in excluded_categories]]
    return render_template('index.html', products=products, categories=categories)

@app.route('/shop')
def shop():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    categories = db.session.query(Product.category.distinct()).all()
    categories = [c[0] for c in categories]
    return render_template('shop.html', products=products, categories=categories, selected_category=category)

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash('All fields are required')
            return render_template('signup.html')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return render_template('signup.html')
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists')
            return render_template('signup.html')
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_to_cart', methods=['POST'])
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id=None):
    if product_id is None:
        data = request.get_json()
        product_id = data['product_id']
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id)
        db.session.add(cart_item)
    db.session.commit()
    flash('Product added to cart successfully!')
    if request.is_json:
        return '', 204
    # Check if we came from product details page
    referer = request.headers.get('Referer', '')
    if '/product/' in referer:
        return redirect(url_for('product_details', product_id=product_id))
    return redirect(url_for('shop'))

@app.route('/remove_from_cart', methods=['POST'])
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id=None):
    if product_id is None:
        data = request.get_json()
        product_id = data['product_id']
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
        db.session.commit()
    if request.is_json:
        return '', 204
    return redirect(url_for('cart'))

@app.route('/delete_from_cart/<int:product_id>', methods=['POST'])
@login_required
def delete_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
@login_required
def clear_cart():
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    if request.is_json:
        return '', 204
    return redirect(url_for('cart'))

@app.route('/cart_count')
def cart_count():
    if current_user.is_authenticated:
        count = db.session.query(db.func.sum(CartItem.quantity)).filter_by(user_id=current_user.id).scalar() or 0
    else:
        count = 0
    return {'count': count}

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_details.html', product=product)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty')
        return redirect(url_for('cart'))
    
    if request.method == 'POST':
        # Get form data
        shipping_name = request.form.get('shipping_name')
        shipping_email = request.form.get('shipping_email')
        shipping_address = request.form.get('shipping_address')
        shipping_city = request.form.get('shipping_city')
        shipping_zipcode = request.form.get('shipping_zipcode')
        shipping_phone = request.form.get('shipping_phone')
        payment_method = request.form.get('payment_method')
        
        # Validate required fields
        if not all([shipping_name, shipping_email, shipping_address, shipping_city, shipping_zipcode, shipping_phone, payment_method]):
            flash('Please fill in all required fields')
            return redirect(url_for('checkout'))
        
        # Calculate total
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            shipping_name=shipping_name,
            shipping_email=shipping_email,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_zipcode=shipping_zipcode,
            shipping_phone=shipping_phone,
            payment_method=payment_method,
            created_at=datetime.utcnow()
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
        
        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        
        # Commit all changes
        db.session.commit()
        
        flash('Your order has been placed successfully! Order ID: #' + str(order.id))
        return redirect(url_for('index'))
    
    # Calculate total for display
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total, user=current_user)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not all([name, email, subject, message]):
            flash('Please fill in all required fields')
            return redirect(url_for('contact'))
        
        # Here you would typically send an email or save to database
        # For now, we'll just show a success message
        flash('Thank you for contacting us! We will get back to you soon.')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/category/<category_name>')
def category_page(category_name):
    products = Product.query.filter_by(category=category_name).all()
    if not products:
        flash('No products found in this category')
        return redirect(url_for('shop'))
    return render_template('category.html', products=products, category_name=category_name)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        flash('Please enter a search term')
        return redirect(url_for('shop'))
    
    # Search in product name and category (case-insensitive)
    # SQLite LIKE is case-insensitive for ASCII, but using func.lower for cross-database compatibility
    from sqlalchemy import func
    search_term = f'%{query.lower()}%'
    products = Product.query.filter(
        db.or_(
            func.lower(Product.name).like(search_term),
            func.lower(Product.category).like(search_term)
        )
    ).all()
    
    return render_template('search.html', products=products, query=query, results_count=len(products))

if __name__ == '__main__':
    app.run(debug=True)