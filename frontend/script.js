window.addEventListener("scroll", function() {
    const navbar = document.querySelector(".navbar");
    if (window.scrollY > 50) {
        navbar.classList.add("scrolled");
        document.querySelector(".vacation").style.color = "#6FB1FC";
        document.querySelectorAll(".nav-links a").forEach(link => link.style.color = "black");
        document.querySelector(".signup-btn").style.borderColor = "#6FB1FC";
    } else {
        navbar.classList.remove("scrolled");
        document.querySelector(".vacation").style.color = "white";
        document.querySelectorAll(".nav-links a").forEach(link => link.style.color = "white");
        document.querySelector(".signup-btn").style.borderColor = "white";
    }
});
