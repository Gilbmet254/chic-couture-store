const API = "https://chic-couture-api.onrender.com";

const output = document.getElementById("output");

async function loadProducts() {
    output.innerHTML = "<p>Loading products...</p>";

    try {
        const res = await fetch(`${API}/products`);

        console.log("Products API Status:", res.status);

        if (!res.ok) {
            throw new Error(`API Error: ${res.status} ${res.statusText}`);
        }

        const data = await res.json();

        if (!Array.isArray(data)) {
            throw new Error("Invalid data format received from API");
        }

        output.innerHTML = `
            <h2>Products</h2>
            <div class="grid">
                ${data.map(p => `
                    <div class="card">
                        <h3>${p.name}</h3>
                        <p>Price: $${p.price}</p>
                        <p>Category: ${p.category}</p>
                    </div>
                `).join("")}
            </div>
        `;

    } catch (err) {
        console.error("Load Products Error:", err);

        output.innerHTML = `
            <h2>Products</h2>
            <p style="color:red;">
                ❌ Failed to load products<br>
                <strong>Reason:</strong> ${err.message}
            </p>
        `;
    }
}

// placeholder for now (we’ll connect later)
function loadOrders() {
    output.innerHTML = `
        <h2>Orders</h2>
        <p>Not connected yet</p>
    `;
}

function loadCustomers() {
    output.innerHTML = `
        <h2>Customers</h2>
        <p>Not connected yet</p>
    `;
}
