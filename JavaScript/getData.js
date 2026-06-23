let productsContainer=[];
let allProducts=[]; // Store all products for cart functionality
let linkName=document.getElementsByClassName("categories_link");

getData()
async function getData(category = null){
    showLoading();
    try {
        let response = await fetch('json/products.json');
        let json=await response.json();
        allProducts=json; // Store all products
        productsContainer=json;
        // Also update the products array in cart.js
        if (typeof products !== 'undefined') {
            products = json;
        }
        if (category) {
            productsContainer = productsContainer.filter(product => product.category === category);
        }
        displayProducts();
    } catch (error) {
        console.error('Error fetching products:', error);
        showError();
    }
}

function showLoading() {
    const container = document.querySelector('.products .content');
    if (container) {
        container.innerHTML = `
            <div class="loading-container">
                <div class="spinner"></div>
                <p>Loading products...</p>
            </div>
        `;
    }
}

function showError() {
    const container = document.querySelector('.products .content');
    if (container) {
        container.innerHTML = `
            <div class="error-container">
                <ion-icon name="alert-circle-outline"></ion-icon>
                <p>Failed to load products. Please try again.</p>
                <button onclick="getData()" class="retry-btn">Retry</button>
            </div>
        `;
    }
}
function displayProducts(){
    let container=``;
    for(let i=0;i<productsContainer.length;i++ ){
        container+=`
        <div class="product-card" data-id="${productsContainer[i].id}">
        <div class="card-img">
            <img  onclick=displayDetails(${productsContainer[i].id});
             src=${productsContainer[i].images[0]}
             alt=${productsContainer[i].name}>
            <a href=""  class="addToCart">
                <ion-icon name="cart-outline" class="Cart"></ion-icon>
            </a>
        </div>
        <div class="card-info">
             <h4 class="product-name" onclick=displayDetails(${productsContainer[i].id});>${productsContainer[i].name}</h4>
             <h5 class="product-price">$${productsContainer[i].price}</h5>
        </div>
    </div>`
    }
    document.getElementById("productCount").innerHTML = `${productsContainer.length} Products`;
    document.querySelector('.products .content').innerHTML = container;
      // Adding event listener to each "addToCart" link
      let addToCartLinks = document.querySelectorAll('.addToCart');
      addToCartLinks.forEach(link => {
          link.addEventListener('click', function(event) {
              event.preventDefault();
              event.stopPropagation();
              let productCard = event.target.closest('.product-card');
              if (productCard && productCard.dataset.id) {
                  let id_product = productCard.dataset.id;
                  // Find the product from the full products list
                  let product = allProducts.find(p => p.id == id_product);
                  if (product) {
                      // Update the global products array for cart.js
                      if (typeof products !== 'undefined') {
                          products = allProducts;
                      }
                      addToCart(id_product);
                  } else {
                      showToast('Product not found', 'info');
                  }
              }
          });
      });
}
function getCategory(e){
    let category = e.target.getAttribute('productCategory');
    setActiveLink(e.target)
    try{
        getData(category);
    }catch(e){
        console.log("not found")
    }
    if (window.innerWidth <= 768) {
        // to close when use select category
        toggleSidebar();
    }
}
function setActiveLink(activeLink) {
    Array.from(linkName).forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

Array.from(linkName).forEach(function(element){
    element.addEventListener('click',getCategory);
})

function toggleSidebar() {
    var sidebar = document.querySelector(".aside");
    sidebar.classList.toggle("open");
}

function displayDetails(productId){
    window.location.href = `ProductDetails.html?productId=${productId}`;
}
