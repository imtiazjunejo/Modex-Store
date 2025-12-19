const products = [
  { id: 1, name: "Classic T-Shirt", price: 15.99, image: "images/tshirt1.jpg" },
  { id: 2, name: "Cool Hoodie", price: 29.99, image: "images/hoodie1.jpg" },
  { id: 3, name: "Denim Jeans", price: 34.99, image: "images/jeans1.jpg" },
  { id: 4, name: "Stylish Cap", price: 12.99, image: "images/cap1.jpg" }
];

const productList = document.getElementById("product-list");
if (productList) {
  productList.innerHTML = products.map(product => `
    <div class="product">
      <img src="${product.image}" alt="${product.name}">
      <h3>${product.name}</h3>
      <p>$${product.price.toFixed(2)}</p>
      <button onclick="addToCart(${product.id})">Add to Cart</button>
    </div>
  `).join('');
}
