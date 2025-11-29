// quantity buttons

function changeQty(btn, val) {
    let input = btn.parentNode.querySelector(".quantity");
    let num = parseInt(input.value) + val;
    input.value = Math.max(1, num);
}



//add to cart

function addToCart(button) {
    const card = button.closest(".card");
    const menu_id = card.dataset.id;
    const quantity = card.querySelector(".quantity").value;

    fetch("/ajax/add-to-cart/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
        },
        body: new URLSearchParams({
            menu_id: menu_id,
            quantity: quantity,
        }),
    })
    .then(res => res.json())
    .then(data => {
        refreshCart();
        document.querySelector(".cart").style.display = "block";
        
    });


     
}






let offset = 8;

document.getElementById("view-more-btn")?.addEventListener("click", function () {

    fetch(`/ajax/load-more/?offset=${offset}`)
    .then(res => res.json())
    .then(data => {

        data.items.forEach(item => {
            const html = `
            <div class="card" data-id="${item.menuID}">
                <img src="/static/${item.image_url}" alt="${item.menuName}">
                <h3 class="food-name">${item.menuName}</h3>
                <p class="price">Rs ${item.price}</p>

                <div class="quantity-container">
                    <button class="qty-btn" onclick="changeQty(this, -1)">-</button>
                    <input type="number" class="quantity" value="1" min="1">
                    <button class="qty-btn" onclick="changeQty(this, 1)">+</button>
                </div>

                <button class="add-cart-btn" onclick="addToCart(this)">Add to Cart</button>
            </div>`;

            document.getElementById("menu-container").insertAdjacentHTML("beforeend", html);
        });

        offset += 8;
    });
});
// display items and total amount
function refreshCart() {
    fetch("/ajax/get-cart/")
    .then(res => res.json())
    .then(data => {
        const tableBody = document.querySelector("#cart-items tbody"); 
        tableBody.innerHTML = ""; // clear old rows

        let total = 0;

        data.items.forEach(item => {
            const row = document.createElement("tr"); // create a table row

            // name column
            const nameCell = document.createElement("td");
            nameCell.textContent = item.name;
            row.appendChild(nameCell);

            // quantity column
            const qtyCell = document.createElement("td");
            qtyCell.textContent = item.qty;
            row.appendChild(qtyCell);

            // subtotal column
            const subtotalCell = document.createElement("td");
            subtotalCell.textContent = item.subtotal;
            row.appendChild(subtotalCell);

            // action column (remove button)
            const actionCell = document.createElement("td"); 
            const removeBtn = document.createElement("button"); 
            removeBtn.textContent = "-"; // label
            removeBtn.classList.add("remove-btn");
            removeBtn.addEventListener("click", () => {
                removeFromCart(item.menuID); // call remove function with item name
            });
            actionCell.appendChild(removeBtn);
            row.appendChild(actionCell);

            tableBody.appendChild(row);

            total += item.subtotal;
        });

        
        document.getElementById("cart-total").textContent = `Total: Rs ${total}`;
          
        updateConfirmButton();

    });
}





function removeFromCart(menu_id) {
    fetch("/ajax/remove-from-cart/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),                 
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({ menu_id: menu_id })    
    })
    .then(res => res.json())
    .then(data => {
        refreshCart(); 
    });
}



function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
           
            if (cookie.substring(0, "csrftoken=".length) === "csrftoken=") {
                cookieValue = decodeURIComponent(cookie.substring("csrftoken=".length));
                break;
            }
        }
    }
    return cookieValue;
}







document.getElementById("refresh-cart").addEventListener("click", function () {
    fetch("/ajax/clear-cart/", {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() }
    })
    .then(res => res.json())
    .then(data => {
        document.querySelector("#cart-items tbody").innerHTML = "";
        document.getElementById("cart-total").textContent = "Total: Rs 0";
        document.querySelector(".cart").style.display = "none";
        document.getElementById("delivery-modal").style.display = "none";
        alert(data.message);
        
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const orderBtn = document.getElementById("order-btn");
    if (orderBtn) {
        orderBtn.addEventListener("click", function () {
            
        document.getElementById("delivery-mode").value = "";

        
        document.getElementById("deliveryaddressbox").style.display = "none";

         
        document.getElementById("delivery-address").value = "";

       
        document.getElementById("delivery-modal").style.display = "block";
         });
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const closeBtn = document.getElementById("close-modal");
    if (closeBtn) {
        closeBtn.addEventListener("click", function () {
            document.getElementById("delivery-modal").style.display = "none";
        });
    }
});




document.getElementById("delivery-mode").addEventListener("change", function () {
  if (this.value === "delivery") {
    document.getElementById("deliveryaddressbox").style.display = "block";
  } else {
    document.getElementById("deliveryaddressbox").style.display = "none";
    document.getElementById("delivery-address").value = ""; 
  }
});




document.getElementById("confirm-order").addEventListener("click", function () {
  const mode = document.getElementById("delivery-mode").value;
  let address = "";

  if (mode === "pickup" ) {
   
    address = ""; }
  else if (mode === "dinein" ) {
   
    address = "";

  } else if  (mode === "delivery") {
    
    address = document.getElementById("delivery-address").value.trim();
    if (!address) {
      alert("Please enter your delivery address.");
      return;
    }
  }
  
 
  
  fetch("/ajax/confirm-order/", {
    method: "POST",
    headers: { "X-CSRFToken": getCSRFToken() },
    body: new URLSearchParams({
      delivery_mode: mode,
      delivery_address: address,
      
    })
  })
  .then(res => res.json().then(data => ({status: res.status, body: data})))
  .then(({status, body}) => {
    if (status === 200) {
      alert(body.message);
    
      document.querySelector("#cart-items tbody").innerHTML = "";
      document.getElementById("cart-total").textContent = "Total: Rs 0";
      document.querySelector(".cart").style.display = "none";
      document.getElementById("delivery-modal").style.display = "none";
    } else {
      
      alert(body.error);
    }
  })
  .catch(err => {
    console.error("Error confirming order:", err);
    alert("Something went wrong while confirming your order.");
  });
});



function updateConfirmButton() {
  const cartHasItems = document.querySelector("#cart-items tbody").children.length > 0;
  document.getElementById("confirm-order").disabled = !cartHasItems;
}


/*  */