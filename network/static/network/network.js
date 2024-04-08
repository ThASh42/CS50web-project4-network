
document.addEventListener("DOMContentLoaded", () => {
    const newPostForm = document.querySelector("#add-new-post-form");

    // By default
    newPostForm.style.display = "none";
    
    document.querySelector("#add-new-post-button").onclick = () => {
        newPostForm.style.display = "block";
    }
})