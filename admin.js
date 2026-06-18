const API = "https://chic-couture-store-api.onrender.com";

const output = document.getElementById("output");
const badge = document.getElementById("notifBadge");

// ======================
// DASHBOARD CHART
// ======================
function loadDashboard() {
    output.innerHTML = "<h2>Dashboard</h2>";

    fetch(`${API}/admin/products`)
        .then(res => res.json())
        .then(data => {
            const categories = {};

            data.forEach(p => {
                categories[p.category || "Other"] =
                    (categories[p.category || "Other"] || 0) + 1;
            });

            const ctx = document.getElementById("chart");

            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: Object.keys(categories),
                    datasets: [{
                        data: Object.values(categories)
                    }]
                }
            });
        });
}

// ======================
// LOAD PRODUCTS
// ======================
async function loadProducts() {
    const res = await fetch(`${API}/admin/products`);
    const data = await res.json();

    output.innerHTML = `
        <h2>Products</h2>
        <div class="grid">
            ${data.map(p => `
                <div class="card">
                    <h3>${p.name}</h3>
                    <p>$${p.price}</p>
                    <p>${p.category || ""}</p>
                    <button 
onclick="deleteProduct(${p.id})">Delete</button>
                </div>
            `).join("")}
        </div>
    `;
}

// ======================
// ADD PRODUCT
// ======================
async function addProduct() {
    const product = {
        name: name.value,
        price: price.value,
        category: category.value,
        description: description.value,
        image: image.value
    };

    const res = await fetch(`${API}/admin/products`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(product)
    });

    if (res.ok) {
        alert("Product added!");
        loadProducts();
        loadDashboard();
    } else {
        alert("Failed");
    }
}

// ======================
// DELETE
// ======================
async function deleteProduct(id) {
    await fetch(`${API}/admin/products/${id}`, {
        method: "DELETE"
    });

    loadProducts();
}

// ======================
// CUSTOMERS + NOTIF
// ======================
async function loadCustomers() {
    const res = await fetch(`${API}/admin/customers`);
    const data = await res.json();

    badge.innerText = data.length; // simple notification idea

    output.innerHTML = `
        <h2>Customers</h2>
        ${data.map(c => `
            <div class="card">
                <p>${c.name}</p>
                <p>${c.email}</p>
            </div>
        `).join("")}
    `;
}

// INIT
loadProducts();
