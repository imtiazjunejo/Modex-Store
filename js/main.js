// Cart logic
let cart = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(id) {
  const product = products.find(p => p.id === id);
  const existing = cart.find(item => item.id === id);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ ...product, qty: 1 });
  }
  saveCart();
  updateCartCount();
  alert(`${product.name} added to cart!`);
}

function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart));
}

function updateCartCount() {
  const countElem = document.getElementById("cart-count");
  if (countElem) countElem.textContent = cart.reduce((a, b) => a + b.qty, 0);
}

function renderCart() {
  const cartItems = document.getElementById("cart-items");
  const totalElem = document.getElementById("cart-total");
  if (!cartItems) return;

  if (cart.length === 0) {
    cartItems.innerHTML = "<p>Your cart is empty.</p>";
    totalElem.textContent = "0.00";
    return;
  }

  cartItems.innerHTML = cart.map(item => `
    <div class="cart-item">
      <span>${item.name} (x${item.qty})</span>
      <span>$${(item.price * item.qty).toFixed(2)}</span>
      <button onclick="removeItem(${item.id})">Remove</button>
    </div>
  `).join('');

  const total = cart.reduce((a, b) => a + b.price * b.qty, 0);
  totalElem.textContent = total.toFixed(2);
}

function removeItem(id) {
  cart = cart.filter(item => item.id !== id);
  saveCart();
  updateCartCount();
  renderCart();
}

document.getElementById("clear-cart")?.addEventListener("click", () => {
  cart = [];
  saveCart();
  updateCartCount();
  renderCart();
});

// Navbar mobile toggle
document.getElementById("menu-toggle")?.addEventListener("click", () => {
  document.getElementById("nav-links").classList.toggle("active");
});

// Initialize on load
updateCartCount();
renderCart();





// ===== Navbar toggle =====
const menuToggle = document.getElementById('menu-toggle');
const navLinks = document.getElementById('nav-links');

menuToggle.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});

// ===== Cart functionality =====
let cartCount = 0;
const cartCountSpan = document.getElementById('cart-count');
const addToCartButtons = document.querySelectorAll('.add-to-cart');

// Optional: Store cart items if you want
let cartItems = [];

addToCartButtons.forEach(button => {
  button.addEventListener('click', () => {
    const productBox = button.parentElement;
    const productName = productBox.querySelector('h3').innerText;
    const productPrice = productBox.querySelector('p').innerText;

    // Increment cart count
    cartCount++;
    cartCountSpan.innerText = cartCount;

    // Add product to cart array (optional)
    cartItems.push({
      name: productName,
      price: productPrice
    });

    alert(`${productName} added to cart!`);
  });
});



