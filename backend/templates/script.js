document.addEventListener("DOMContentLoaded", function () {
    // Navbar scroll effect
    window.addEventListener("scroll", function () {
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

    // Update footer year
    document.getElementById("year").textContent = new Date().getFullYear();

    // Smooth scrolling when clicking navigation links
    document.querySelectorAll('.nav-links a').forEach(anchor => {
        anchor.addEventListener("click", function (event) {
            event.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 50, // Adjust offset for fixed navbar
                    behavior: "smooth"
                });
            }
        });
    });
});

function switchForm(formType) {
    document.getElementById("signup-form").classList.toggle("hidden", formType !== "signup");
    document.getElementById("login-form").classList.toggle("hidden", formType !== "login");

    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.classList.toggle("active", btn.textContent.toLowerCase() === formType);
    });
}

