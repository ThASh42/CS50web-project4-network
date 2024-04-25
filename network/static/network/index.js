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

    document.querySelectorAll(".like-button").forEach(button => {
        const postId = button.dataset.postid;
        const isLiked = like_post_data[postId];
        if (isLiked) button.innerHTML = "Unlike";
        button.onclick = () => likeUnlike(isLiked, postId, button);
    });

    // Unpluralize user text if the counter is 1
    document.querySelectorAll(".span-like").forEach(span => {
        if (span.querySelector(".post-like-count").textContent == 1) 
        span.querySelector(".users-text").textContent = "user";
    });
});

// Edit post button functionality
function editPost(postId) {
    if (editMode === false){
        editMode = true;

        const editTextarea = document.createElement("textarea");
        const editTextareaDiv = document.createElement("div");
        const editPostDiv = document.querySelector(`div[data-postId="${postId}"]`);
        const postContent = editPostDiv.querySelector(".post-content");
        const postElements = editPostDiv.querySelector('.post-elements');

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
        editTextarea.id = "edit-post-textarea"
        
        // Append Childs to the main div
        editTextareaDiv.appendChild(editTextarea);
        editTextareaDiv.appendChild(buttonsDiv);
        editTextareaDiv.classList = ["my-3"];
        editTextareaDiv.id = "edit-post-div";

        editPostDiv.appendChild(editTextareaDiv);

        // Hide post content and datetime
        postElements.style.display = "none";

        closeButton.onclick = () => {
            document.getElementById("edit-post-div").remove();
            editMode = false;
            postElements.style.display = "block";
        };

        editButton.onclick = () => {
            // Edit post textare with new content
            documentEditTextarea = document.getElementById("edit-post-textarea");
            // New content
            new_content = documentEditTextarea.value;
            fetch(`edit-post/${postId}`, {
                method: "PUT",
                body: JSON.stringify({
                    post_content: new_content,
                }),
            });
            // Change post content
            postContent.innerHTML = new_content;
            // Delete edit post block
            document.getElementById("edit-post-div").remove();
            editMode = false;
            postElements.style.display = "block";
        };
    };
};

// Like or unlike post functionality
function likeUnlike(isLiked, postId, button) {
    method = isLiked ? "DELETE" : "POST";

    fetch(`post-like/${postId}`, {
        method: method,
    })
    .then(() => {
        const postDiv = document.querySelector(`div[data-postId="${postId}"]`);
        const likeCount = postDiv.querySelector(".post-like-count");
        const usersText = postDiv.querySelector(".users-text");
        
        // Update the like count displayed on the post
        likeCount.innerHTML = isLiked ? parseInt(likeCount.innerHTML) - 1 : parseInt(likeCount.innerHTML) + 1;
        
        // Pluralize user text if like counter ends with 1
        const likeCountLength = likeCount.textContent.length;
        usersText.textContent = likeCount.textContent.charAt(likeCountLength - 1) == 1 ? "user" : "users";

        // Change button text
        button.innerHTML = isLiked ? "Like" : "Unlike";
        
        // Update the button onclick event to toggle like/unlike functionality
        button.onclick = () => likeUnlike(!isLiked, postId, button);
    });
};
