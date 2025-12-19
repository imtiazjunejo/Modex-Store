// Cart logic with server-side
async function addToCart(id) {
  try {
    const response = await fetch('/add_to_cart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: id })
    });
    if (response.ok) {
      updateCartCount();
      alert('Product added to cart!');
    } else {
      alert('Failed to add to cart');
    }
  } catch (error) {
    console.error('Error adding to cart:', error);
  }
}

async function removeItem(id) {
  try {
    const response = await fetch('/remove_from_cart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: id })
    });
    if (response.ok) {
      updateCartCount();
      if (window.location.pathname === '/cart') {
        window.location.reload();
      }
    } else {
      alert('Failed to remove item');
    }
  } catch (error) {
    console.error('Error removing item:', error);
  }
}

async function updateCartCount() {
  try {
    const response = await fetch('/cart_count');
    const data = await response.json();
    const countElem = document.getElementById("cart-count");
    if (countElem) countElem.textContent = data.count;
  } catch (error) {
    console.error('Error updating cart count:', error);
  }
}

document.getElementById("clear-cart")?.addEventListener("click", async () => {
  if (!confirm('Are you sure you want to clear your cart?')) {
    return;
  }
  try {
    const response = await fetch('/clear_cart', {
      method: 'POST'
    });
    if (response.ok) {
      updateCartCount();
      if (window.location.pathname === '/cart') {
        window.location.reload();
      }
    } else {
      alert('Failed to clear cart');
    }
  } catch (error) {
    console.error('Error clearing cart:', error);
  }
});

// Navbar mobile toggle
document.getElementById("menu-toggle")?.addEventListener("click", () => {
  document.getElementById("nav-links").classList.toggle("active");
});

// Filter by category
function filterCategory(category) {
  const url = category ? `/shop?category=${encodeURIComponent(category)}` : '/shop';
  window.location.href = url;
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});


// Search functionality
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const searchForm = document.querySelector('.search-form');
  
  // Form validation
  if (searchForm) {
    searchForm.addEventListener('submit', function(e) {
      const query = searchInput.value.trim();
      if (!query) {
        e.preventDefault();
        alert('Please enter a search term');
        searchInput.focus();
      }
    });
  }
});

// Initialize on load
updateCartCount();


