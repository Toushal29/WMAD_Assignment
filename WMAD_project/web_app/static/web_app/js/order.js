/* Qty */
function changeQty(btn, val) {
    let input = btn.parentNode.querySelector(".quantity");
    input.value = Math.max(1, parseInt(input.value) + val);
}

/* Add to Cart */
function addToCart(button) {
    const card = button.closest(".card");
    const id = card.dataset.id;
    const qty = card.querySelector(".quantity").value;

    fetch("/ajax/add-to-cart/", {
        method: "POST",
        headers:{ "X-CSRFToken": getCSRFToken() },
        body: new URLSearchParams({ menu_id:id, quantity:qty })
    })
    .then(() => {
        refreshCart();
        showCart();
    });
}

/* Show / Hide Cart */
function toggleCart() {
    const cart = document.getElementById("cart-dropdown");

    if (cart.style.display === "block") {
        cart.style.display = "none";
    } else {
        cart.style.display = "block";
    }
}

document.getElementById("cart-toggle").onclick = toggleCart;


/* Refresh Cart */
function refreshCart() {
    fetch("/ajax/get-cart/")
    .then(r=>r.json())
    .then(data=>{
        let tbody = document.querySelector("#cart-items tbody");
        tbody.innerHTML = "";

        let total = 0;
        data.items.forEach(item=>{
            total += item.subtotal;

            tbody.insertAdjacentHTML("beforeend", `
                <tr>
                    <td>${item.name}</td>
                    <td>${item.qty}</td>
                    <td>${item.subtotal}</td>
                    <td><button class="remove-btn" onclick="removeFromCart(${item.menuID})">×</button></td>
                </tr>
            `);
        });

        document.getElementById("cart-total").innerText = "Total: Rs " + total;
    });
}

/* Remove Item */
function removeFromCart(id) {
    fetch("/ajax/remove-from-cart/", {
        method:"POST",
        headers:{ "X-CSRFToken":getCSRFToken() },
        body:new URLSearchParams({ menu_id:id })
    })
    .then(() => refreshCart());
}

/* Clear */
document.getElementById("refresh-cart").onclick = ()=>{
    fetch("/ajax/clear-cart/", {
        method:"POST",
        headers:{ "X-CSRFToken":getCSRFToken() }
    }).then(()=>refreshCart());
};

/* CSRF */
function getCSRFToken() {
    return document.cookie.split("; ").find(row=>row.startsWith("csrftoken="))?.split("=")[1];
}
