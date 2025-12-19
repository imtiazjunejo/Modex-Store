import requests
from bs4 import BeautifulSoup

base_url = 'http://localhost:5000'
session = requests.Session()
results = []

def log_result(test, success, details=""):
    status = 'PASS' if success else 'FAIL'
    results.append(f"{test}: {status} {details}")

# Test 1: Access home page, verify products display
response = session.get(base_url + '/')
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='product-box')
    if products:
        log_result("Access home page", True, f"Found {len(products)} products")
    else:
        log_result("Access home page", False, "No products found")
else:
    log_result("Access home page", False, f"Status {response.status_code}")

# Test 2: Signup a new user
data = {'username': 'testuser123', 'email': 'test@example.com', 'password': 'password123'}
response = session.post(base_url + '/signup', data=data, allow_redirects=False)
if response.status_code == 302 and 'login' in response.headers.get('Location', ''):
    log_result("Signup a new user", True)
else:
    log_result("Signup a new user", False, f"Status {response.status_code}")

# Test 3: Login with the user
data = {'username': 'testuser123', 'password': 'password123'}
response = session.post(base_url + '/login', data=data, allow_redirects=False)
if response.status_code == 302 and response.headers.get('Location', '').endswith('/'):
    log_result("Login with the user", True)
else:
    log_result("Login with the user", False, f"Status {response.status_code}")

# Test 4: Add items to cart from shop page, verify cart count updates
response = session.get(base_url + '/shop')
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    product_boxes = soup.find_all('div', class_='product-box')
    if product_boxes:
        form = product_boxes[0].find('form')
        action = form['action']
        product_id = action.split('/')[-1]
        response = session.post(base_url + action, allow_redirects=False)
        if response.status_code == 302:
            log_result("Add items to cart from shop page", True)
            # Verify cart count
            response = session.get(base_url + '/cart_count')
            if response.status_code == 200:
                count_data = response.json()
                count = count_data.get('count', 0)
                if count > 0:
                    log_result("Verify cart count updates", True, f"Count: {count}")
                else:
                    log_result("Verify cart count updates", False, "Count not increased")
            else:
                log_result("Verify cart count updates", False, f"Count status {response.status_code}")
        else:
            log_result("Add items to cart from shop page", False, f"Add status {response.status_code}")
    else:
        log_result("Add items to cart from shop page", False, "No products in shop")
else:
    log_result("Add items to cart from shop page", False, f"Shop status {response.status_code}")

# Test 5: View cart page, verify items and total
response = session.get(base_url + '/cart')
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    cart_items = soup.find_all('div', class_='cart-item')
    total_span = soup.find('span', id='cart-total')
    if cart_items and total_span:
        total_text = total_span.text.strip()
        log_result("View cart page", True, f"Items: {len(cart_items)}, Total: {total_text}")
    else:
        log_result("View cart page", False, "Missing items or total")
else:
    log_result("View cart page", False, f"Status {response.status_code}")

# Test 6: Remove items from cart
if 'product_id' in locals():
    response = session.get(base_url + '/cart')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        cart_items = soup.find_all('div', class_='cart-item')
        if cart_items:
            form = cart_items[0].find('form')
            action = form['action']
            response = session.post(base_url + action, allow_redirects=False)
            if response.status_code == 302:
                log_result("Remove items from cart", True)
            else:
                log_result("Remove items from cart", False, f"Remove status {response.status_code}")
        else:
            log_result("Remove items from cart", False, "No items to remove")
    else:
        log_result("Remove items from cart", False, f"Cart status {response.status_code}")
else:
    log_result("Remove items from cart", False, "No product id")

# Test 7: Logout and verify cart is protected
response = session.get(base_url + '/logout', allow_redirects=False)
if response.status_code == 302:
    log_result("Logout", True)
    # Verify cart protected
    response = session.get(base_url + '/cart', allow_redirects=False)
    if response.status_code == 302 and 'login' in response.headers.get('Location', ''):
        log_result("Verify cart is protected", True)
    else:
        log_result("Verify cart is protected", False, f"Cart status {response.status_code}")
else:
    log_result("Logout", False, f"Logout status {response.status_code}")

# Print results
print("Test Results:")
for result in results:
    print(result)