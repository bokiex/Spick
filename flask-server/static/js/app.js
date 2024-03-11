const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const BASE_URL = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;

sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
});

document.addEventListener("DOMContentLoaded", function(){
    const signUpForm = document.querySelector(".sign-up-form");
    const signInForm = document.querySelector(".sign-in-form");

    signUpForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const username = signUpForm.querySelector('input[placeholder="Username"]').value;
        const email = signUpForm.querySelector('input[placeholder="Email"]').value;
        const password = signUpForm.querySelector('input[placeholder="Password"]').value;

        fetch(`${BASE_URL}/signup`,{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
            }),
        })
        .then((response) => response.json())
        .then((data)=>{
            alert(data.message);
            if (data.message === "Account created successfully"){
                window.location.href = '/login.html';
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    });

    signInForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const username = signInForm.querySelector('input[placeholder="Username"]').value;
        const password = signInForm.querySelector('input[placeholder="Password"]').value;
        
        fetch(`${BASE_URL}/login`,{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        })
        .then((response) => response.json())
        .then((data)=>{
            alert(data.message);
            if (data.message === "Logged in successfully"){
                window.location.href = '/main.html';
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    });
});