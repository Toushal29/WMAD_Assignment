/* TOGGLE CART */
const toggleBtn = document.getElementById("cart-toggle");
const dropdown = document.getElementById("cart-dropdown");
const closeBtn = document.getElementById("close-cart");
const countBadge = document.getElementById("cart-count");

if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
        dropdown.style.display =
            dropdown.style.display === "block" ? "none" : "block";
    });
}

if (closeBtn) {
    closeBtn.addEventListener("click", () => {
        dropdown.style.display = "none";
    });
}

/* REFRESH CART CONTENT */
function refreshCart() {
    fetch("/ajax/get-cart/")
        .then(res => res.json())
        .then(data => {
            let tbody = document.querySelector("#cart-items tbody");
            tbody.innerHTML = "";

            let total = 0;
            let itemsCount = data.items.length;

            data.items.forEach(item => {
                total += item.subtotal;
                tbody.insertAdjacentHTML("beforeend", `
                    <tr>
                        <td>${item.name}</td>
                        <td>x${item.qty}</td>
                        <td>Rs ${item.subtotal}</td>
                        <td><button class="remove-btn" onclick="removeFromCart(${item.menuID})">×</button></td>
                    </tr>
                `);
            });

            document.getElementById("cart-total").innerHTML = "Total: Rs " + total;

            /* UPDATE COUNTER */
            if (itemsCount > 0) {
                countBadge.style.display = "block";
                countBadge.innerText = itemsCount;
            } else {
                countBadge.style.display = "none";
            }
        });
}

/* ADD ITEM */
function addToCart(button) {
    const card = button.closest(".card");
    const id = card.dataset.id;
    const qty = card.querySelector(".quantity").value;

    fetch("/ajax/add-to-cart/", {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() },
        body: new URLSearchParams({ menu_id: id, quantity: qty })
    }).then(() => {
        refreshCart();
        dropdown.style.display = "block";  // auto open cart
    });
}

/* REMOVE ITEM */
function removeFromCart(id) {
    fetch("/ajax/remove-from-cart/", {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() },
        body: new URLSearchParams({ menu_id: id })
    }).then(refreshCart);
}

/* CLEAR CART */
document.getElementById("refresh-cart").onclick = () => {
    fetch("/ajax/clear-cart/", {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() }
    }).then(refreshCart);
};

/* CHECKOUT */
document.getElementById("checkout-btn").onclick = () => {
    window.location.href = "/checkout/";
};

/* GET CSRF */
function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

function changeQty(btn, val) {
    let input = btn.parentNode.querySelector(".quantity");
    let num = parseInt(input.value) + val;
    input.value = Math.max(1, num);
    console.log("Button clicked!", val, "New value:", input.value);
}


/* INITIAL CART LOAD */
refreshCart();
