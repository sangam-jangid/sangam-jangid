const slider = document.getElementById('snackSlider');

let scrollAmount = 0;
let scrollStep = 400; // adjust how much to scroll per step
let maxScroll = slider.scrollWidth - slider.clientWidth;

setInterval(() => {
  if (scrollAmount >= maxScroll) {
    scrollAmount = 0;
  } else {
    scrollAmount += scrollStep;
  }
  slider.scrollTo({
    left: scrollAmount,
    behavior: 'smooth'
  });
}, 2000); 

const biscuitSlider = document.getElementById('biscuitSlider');
let biscuitScrollAmount = 0;
let biscuitScrollStep = 400;
let biscuitMaxScroll = biscuitSlider.scrollWidth - biscuitSlider.clientWidth;

setInterval(() => {
  if (biscuitScrollAmount >= biscuitMaxScroll) {
    biscuitScrollAmount = 0;
  } else {
    biscuitScrollAmount += biscuitScrollStep;
  }
  biscuitSlider.scrollTo({
    left: biscuitScrollAmount,
    behavior: 'smooth'
  });
}, 2000);



let Count = 0

  function showCounter(addBtnId, counterDivId) {
    document.getElementById(addBtnId).classList.add("hidden");
    let counterDiv = document.getElementById(counterDivId);
    counterDiv.classList.remove("hidden");
    counterDiv.classList.add("flex");  // Ensure flex is applied when showing
  }
  
  function increment(counterValueId) {
    let count = document.getElementById(counterValueId);
    count.innerText = parseInt(count.innerText) + 1;
  }
  
  function decrement(counterValueId, counterDivId, addBtnId) {
    let count = document.getElementById(counterValueId);
    let value = parseInt(count.innerText);
    if (value > 1) {
      count.innerText = value - 1;
    } else {
      let counterDiv = document.getElementById(counterDivId);
      counterDiv.classList.add("hidden");
      counterDiv.classList.remove("flex"); // Remove flex when hiding
      document.getElementById(addBtnId).classList.remove("hidden");
    }
  }

document.querySelectorAll(".buttons").forEach((button) => {
  button.addEventListener("click", () => {
    const popup = document.getElementById("popupMessage");
    popup.classList.remove("opacity-0");
    popup.classList.add("opacity-100");
  });
});
  
let Increment = document.querySelectorAll(".increment")
let Decrement = document.querySelectorAll(".decrement")
let CounterDiv1 = document.querySelectorAll(".counterDiv1")
let Quantity = document.getElementById("quantity")
let buttons = document.querySelectorAll(".buttons")


Increment.forEach((inc) => {
  inc.addEventListener('click', ()=>{
    Count++
    quantity.innerText = `Item added: ${Count}`
  })
})

Decrement.forEach((dec) =>{
  dec.addEventListener('click', ()=>{
    Count--
    quantity.innerText = `Item added: ${Count}`
    if(Count==0){
      const popup = document.getElementById("popupMessage");
      popup.classList.add('hidden')
      popup.classList.remove('flex')
}
  })
})

buttons.forEach((b) =>{
  b.addEventListener('click', ()=>{
    Count++
    quantity.innerText = `Item added: ${Count}`
    const popup = document.getElementById("popupMessage");
    popup.classList.add('flex')
    popup.classList.remove('hidden')
  })
})

let cart = []

const addBtn = document.querySelectorAll(".buttons").forEach((btn) =>{
  btn.addEventListener('click', ()=>{
    const id = btn.dataset.id
    const name = btn.dataset.name
    const price = btn.dataset.price

    cart.push({id, name, price, quantity:1})
    console.log(cart)
  })
})

document.querySelectorAll(".increment").forEach((inc) => {
  inc.addEventListener("click", () => {
    const id = inc.dataset.id;
    const name = inc.dataset.name;
    const price = inc.dataset.price;

    const existingItem = cart.find(item => item.id === id);
    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      cart.push({
        id,
        name,
        price,
        quantity: 1
      });
    }

    console.log(cart);
  });
});


document.querySelectorAll(".decrement").forEach((dec) => {
  dec.addEventListener("click", () => {
    const id = dec.dataset.id;

    const index = cart.findIndex(item => item.id === id);

    if (index !== -1) {
      if (cart[index].quantity > 1) {
        cart[index].quantity -= 1;
      } else {
        cart.splice(index, 1);
      }
    }

    cart.forEach((e) =>{
      console.log(e.dataset.id)
    })
  });
});


