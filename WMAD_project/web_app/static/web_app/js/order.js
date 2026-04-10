// C:\Users\...\WMAD_Assignment\WMAD_project\web_app\static\web_app\js\order.js

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

function refreshCart() {
    fetch("/ajax/get-cart/")
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById("cart-items");
            container.innerHTML = "";

            let total = 0;
            const itemsCount = data.items.length;

            data.items.forEach(item => {
                total += item.subtotal;
                container.insertAdjacentHTML("beforeend", `
                <div class="cart-item">
                    <span>${item.name}</span>
                    <span>x${item.qty}</span>
                    <button onclick="removeFromCart(${item.menu_id})">X</button>
                </div>
            `);
            });

            document.getElementById("cart-total").innerHTML = "Total: Rs " + total;

            if (itemsCount > 0) {
                countBadge.style.display = "block";
                countBadge.innerText = itemsCount;
            } else {
                countBadge.style.display = "none";
            }
        });
}

if (closeBtn) {
    closeBtn.addEventListener("click", () => {
        dropdown.style.display = "none";
    });
}

function addToCart(button) {
    const card = button.closest(".card");
    const id = card.dataset.id;
    const qty = card.querySelector(".quantity").value;

    fetch("/ajax/add-to-cart/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
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

function removeFromCart(id) {
    fetch("/ajax/remove-from-cart/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: new URLSearchParams({
            menu_id: id
        })
    })
        .then(() => {
            refreshCart();
        });
}

const clearBtn = document.getElementById("refresh-cart");

if (clearBtn) {
    clearBtn.onclick = () => {
        fetch("/ajax/clear-cart/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        })
            .then(() => {
                refreshCart();
            });
    };
}

const checkoutBtn = document.getElementById("checkout-btn");
if (checkoutBtn) {
    checkoutBtn.onclick = () => {
        window.location.href = "/checkout/";
    };
}

document.addEventListener("DOMContentLoaded", () => {
    refreshCart();
});

function changeQty(btn, change) {
    const qtyInput = btn.parentElement.querySelector(".quantity");
    let value = parseInt(qtyInput.value, 10) || 1;
    value += change;
    if (value < 1) value = 1;
    qtyInput.value = value;
}


// web_app/static/web_app/js/order.js

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function confirmFinalOrder() {
    const paymentRadios = document.getElementsByName('payment_method');
    if (!paymentRadios.length) return; // prevent errors

    let selectedMethod = 'cash';

    for (const radio of paymentRadios) {
        if (radio.checked) {
            selectedMethod = radio.value;
            break;
        }
    }

    fetch("/ajax/confirm-order/", {
        method: "POST",
        headers: { 
            "X-CSRFToken": getCookie('csrftoken'),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            payment_method: selectedMethod
        })
    })
    .then(res => res.json())
    .then(res => {
        if (res.success) {
            window.location.href = res.redirect;
        }
    })
    .catch(() => {
        alert("Order failed.");
    });
}