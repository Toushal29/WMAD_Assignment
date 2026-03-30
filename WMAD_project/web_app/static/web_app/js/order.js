/* CART TOGGLE */
const toggleBtn = document.getElementById("cart-toggle");
const dropdown = document.getElementById("cart-dropdown");
const countBadge = document.getElementById("cart-count");
const closeBtn = document.getElementById("cart-close");

if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
        dropdown.style.display =
            dropdown.style.display === "block" ? "none" : "block";
    });
}

/* REFRESH CART CONTENT */
function refreshCart() {
    fetch("/ajax/get-cart/")
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById("cart-items");
            container.innerHTML = "";

            let total = 0;
            let itemsCount = data.items.length;

            data.items.forEach(item => {
                total += item.subtotal;
                container.insertAdjacentHTML("beforeend", `
                <div class="cart-item">
                    <span>${item.name}</span>
                    <span>x${item.qty}</span>
                    <button onclick="removeFromCart(${item.menuID})">✕</button>
                </div>
            `);
            });
            document.getElementById("cart-total").innerHTML =
                "Total: Rs " + total;

            /* UPDATE CART COUNTER */
            if (itemsCount > 0) {
                countBadge.style.display = "block";
                countBadge.innerText = itemsCount;
            } else {
                countBadge.style.display = "none";
            }
        });
}

/* Close button */
if (closeBtn) {
    closeBtn.addEventListener("click", () => {
        dropdown.style.display = "none";
    });
}

/* ADD ITEM TO CART */
function addToCart(button) {
    const card = button.closest(".card");
    const id = card.dataset.id;
    const qty = card.querySelector(".quantity").value;

    fetch("/ajax/add-to-cart/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        body: new URLSearchParams({
            menu_id: id,
            quantity: qty
        })
    })

        .then(() => {
            refreshCart();
        });
}

/* REMOVE ITEM */
function removeFromCart(id) {
    fetch("/ajax/remove-from-cart/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        body: new URLSearchParams({
            menu_id: id
        })
    })
        .then(() => {
            refreshCart();
        });
}

/* CLEAR CART */
const clearBtn = document.getElementById("refresh-cart");

if (clearBtn) {
    clearBtn.onclick = () => {
        fetch("/ajax/clear-cart/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken()
            }
        })
            .then(() => {
                refreshCart();
            });
    };
}

/* CHECKOUT BUTTON */
const checkoutBtn = document.getElementById("checkout-btn");
if (checkoutBtn) {
    checkoutBtn.onclick = () => {
        window.location.href = "/checkout/";
    };
}

/* CSRF TOKEN */
function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

/* INITIAL LOAD */
document.addEventListener("DOMContentLoaded", () => {
    refreshCart();
});

/* QUANTITY BUTTONS */
function changeQty(btn, change) {
    const qtyInput = btn.parentElement.querySelector(".quantity");
    let value = parseInt(qtyInput.value) || 1;
    value += change;
    if (value < 1) value = 1;
    qtyInput.value = value;
}