document.addEventListener("DOMContentLoaded", () => {
    const newPostForm = document.querySelector("#add-new-post-form");
    const newPostFormButton = newPostForm.querySelector("button");
    const newPostFormTextarea = newPostForm.querySelector("textarea");

    // By default
    newPostFormButton.disabled = true;

    // By default
    newPostForm.style.display = "none";
    
    document.querySelector("#add-new-post-button").onclick = () => {
        newPostForm.style.display = "block";
    };

    newPostFormTextarea.addEventListener("keyup", () => {
        if (newPostFormTextarea.value === "") {
            newPostFormButton.disabled = true;
        } else {
            newPostFormButton.disabled = false;
        };
    });
})