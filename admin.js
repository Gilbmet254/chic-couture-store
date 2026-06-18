const API = "https://chic-couture-store-api.onrender.com";

const output = document.getElementById("output");

// =======================
// LOAD PRODUCTS
// =======================
async function loadProducts() {
    output.innerHTML = "<p>Loading products...</p>";

    try {
        const res = await fetch(`${API}/admin/products`);
        const data = await res.json();

        if (!Array.isArray(data)) {
            throw new Error("Invalid response from server");
        }

        output.innerHTML = `
            <h2>📦 Products</h2>
            <div class="grid">
                ${data.map(p => `
                    <div class="card">
                        <h3>${p.name}</h3>
                        <p><b>Price:</b> $${p.price}</p>
                        <p><b>Category:</b> ${p.category || "N/A"}</p>
                        <p>${p.description || ""}</p>

                        <button 
onclick="deleteProduct(${p.id})">Delete</button>
                    </div>
                `).join("")}
            </div>
        `;

    } catch (err) {
        output.innerHTML = `<p style="color:red;">${err.message}</p>`;
    }
}

// =======================
// ADD PRODUCT
// =======================
async function addProduct() {
    const product = {
        name: document.getElementById("name").value,
        price: document.getElementById("price").value,
        category: document.getElementById("category").value,
        description: document.getElementById("description").value,
        image: document.getElementById("image").value
    };

    try {
        const res = await fetch(`${API}/admin/products`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(product)
        });

        if (!res.ok) throw new Error("Failed to add product");

        alert("Product added successfully!");
        loadProducts();

    } catch (err) {
        alert(err.message);
    }
}

// =======================
// DELETE PRODUCT
// =======================
async function deleteProduct(id) {
    try {
        const res = await fetch(`${API}/admin/products/${id}`, {
            method: "DELETE"
        });

        if (!res.ok) throw new Error("Delete failed");

        loadProducts();

    } catch (err) {
        alert(err.message);
    }
}

// =======================
// INIT
// =======================
loadProducts();
