const API = "https://chic-couture-store-api.onrender.com";

const output = document.getElementById("output");

// =======================
// LOAD PRODUCTS
// =======================
async function loadProducts() {
    output.innerHTML = "<p>Loading products...</p>";

    try {
        const res = await fetch(`${API}/admin/products`);

        if (!res.ok) {
            throw new Error(`Server error: ${res.status}`);
        }

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

                        <button onclick="deleteProduct(${p.id})">
                            Delete
                        </button>
                    </div>
                `).join("")}
            </div>
        `;

    } catch (err) {
        output.innerHTML = `
            <p style="color:red;">
                ❌ Failed to load products<br>
                ${err.message}
            </p>
        `;
    }
}

// =======================
// ADD PRODUCT (FIXED)
// =======================
async function addProduct() {

    const name = document.getElementById("name").value.trim();
    const price = parseFloat(document.getElementById("price").value);
    const category = document.getElementById("category").value.trim();
    const description = 
document.getElementById("description").value.trim();
    const image = document.getElementById("image").value.trim();

    // validation (VERY IMPORTANT)
    if (!name || isNaN(price)) {
        alert("Please enter valid product name and price");
        return;
    }

    const product = {
        name,
        price,
        category,
        description,
        image
    };

    try {
        const res = await fetch(`${API}/admin/products`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(product)
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.message || "Failed to add product");
        }

        alert("✅ Product added successfully!");

        // clear form after success
        document.getElementById("name").value = "";
        document.getElementById("price").value = "";
        document.getElementById("category").value = "";
        document.getElementById("description").value = "";
        document.getElementById("image").value = "";

        loadProducts();

    } catch (err) {
        alert("❌ " + err.message);
    }
}

// =======================
// DELETE PRODUCT
// =======================
async function deleteProduct(id) {
    if (!confirm("Delete this product?")) return;

    try {
        const res = await fetch(`${API}/admin/products/${id}`, {
            method: "DELETE"
        });

        if (!res.ok) {
            throw new Error("Delete failed");
        }

        loadProducts();

    } catch (err) {
        alert(err.message);
    }
}

// =======================
// INIT
// =======================
loadProducts();
