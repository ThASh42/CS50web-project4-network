document.addEventListener("DOMContentLoaded", () => {
    const newPostForm = document.getElementById("add-new-post-form");
    const newPostFormCreateButton = newPostForm.querySelector("#add-new-post-form-create-button");
    const newPostFormTextarea = newPostForm.querySelector("textarea");

    // By default
    newPostFormCreateButton.disabled = true;

    // By default
    newPostForm.style.display = "none";
    
    // Open and close buttons of new post form
    document.getElementById("add-new-post-form-open-button").onclick = () => {
        newPostForm.style.display = "block";
    };
    document.getElementById("add-new-post-form-close-button").onclick = () => {
        newPostForm.style.display = "none";
    };

    newPostFormTextarea.addEventListener("keyup", () => {
        if (newPostFormTextarea.value === "") {
            newPostFormCreateButton.disabled = true;
        } else {
            newPostFormCreateButton.disabled = false;
        };
    });
})