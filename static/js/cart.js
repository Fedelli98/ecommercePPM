
const updateCartButtons = document.getElementsByTagName('button');

for (let i = 0; i < updateCartButtons.length; i++) {
  const button = updateCartButtons[i];
  const id = button.getAttribute('id');
  if (id === 'updatecart') {
    button.addEventListener('click', function() {
      const productId = this.dataset.product;
      const action = this.dataset.action;
      const customer = this.dataset.customer;

      console.log("productId: " + productId);
      console.log("Customer: " + customer);
      console.log("userId: " + user);
      if(user === 'AnonymousUser'){
        alert("Please login to add to cart");
      }
      else{
        updateUserOrder(productId, action)
      }
    });
  }
}


function updateUserOrder(productId, action) {
  console.log('User is authenticated, sending data...')
  console.log()

  const url = '/update_cart/';

  fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken' : csrftoken,
    },
    body: JSON.stringify({
      "productId": productId,
      "action": action})
  })

  .then((response) => {
    return response.json();
  })

  .then((data) => {
    console.log("data", data)
    location.reload()
  })
}