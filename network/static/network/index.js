var editMode = false;

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
});

// Edit post button functionality
function editPost(postId) {
    if (editMode === false){
        editMode = true;

        const editTextarea = document.createElement("textarea");
        const editTextareaDiv = document.createElement("div");
        const editPostDiv = document.querySelector(`div[data-postId="${postId}"]`);
        const postContent = editPostDiv.querySelector("#post-content");

        // Div of close and edit buttons
        const editButton = document.createElement("button");
        const closeButton = document.createElement("button");
        const buttonsDiv = document.createElement("div");
        editButton.classList = ["btn btn-primary mx-1"]; editButton.innerHTML = "Edit";
        closeButton.classList = ["btn btn-dark mx-1"]; closeButton.innerHTML = "Close";
        buttonsDiv.appendChild(editButton); buttonsDiv.appendChild(closeButton);
        buttonsDiv.classList = ["d-flex justify-content-center my-2"]
        
        // Textarea
        editTextarea.innerHTML = postContent.innerHTML;
        editTextarea.classList = ["form-control"];
        
        // Append Childs to the main div
        editTextareaDiv.appendChild(editTextarea);
        editTextareaDiv.appendChild(buttonsDiv);
        editTextareaDiv.classList = ["my-3"];

        editPostDiv.appendChild(editTextareaDiv);
    };
};
