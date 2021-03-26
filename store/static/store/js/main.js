// slide images
const images = document.querySelectorAll(".slide-img")
const imgContainer = document.querySelector(".slide-image-container")
const circles = document.querySelectorAll(".circle")

let counter = 0
circles[counter].style.background = "red"

imgContainer.addEventListener("mouseenter", function(){
    slide()
})

function slide(){
    counter ++
    circles.forEach(function(circle){
         circle.style.background = "rgb(167, 167, 167)"
    })

    if (counter == images.length-1){
        counter = 0
    }
    images.forEach(function(img){
        img.style.transform = `translate(-${counter*100}%)`
        circles[counter].style.background = "red"
        img.style.transition = "all 3s ease-in-out"
    })
}




// side categories
const category = document.querySelector(".category")
const categories = document.querySelector(".categories")
const timesButton = document.querySelector(".times-button")
const body = document.querySelector("html body")

category.addEventListener("click", function(){
    categories.classList.toggle("show-categories")
    body.style.overflow = "hidden"
})

timesButton.addEventListener("click", function(){
    categories.classList.remove("show-categories")
    body.style.overflow = "scroll"
})
