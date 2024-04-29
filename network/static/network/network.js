var editMode = false;
const likeIcon = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
</svg> ` 
const unlikeIcon = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16">
    <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
</svg> `

document.addEventListener("DOMContentLoaded", () => {
    // Add likeUnlike function to all like buttons
    document.querySelectorAll(".like-button").forEach(button => {
        const postId = button.dataset.postid;
        const isLiked = like_post_data[postId];
        if (isLiked) button.innerHTML = unlikeIcon;
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
        // Enter edit mode
        editMode = true;
        const postEditDiv = document.createElement("div");
        const postDiv = document.querySelector(`div[data-postId="${postId}"]`);
        const postElements = postDiv.querySelector(".post-elements");
        const postContent = postElements.querySelector(".post-content");

        postEditDiv.id = "edit-post-div"; 
        postEditDiv.className = "my-3";

        // Fill and display postEditDiv
        postEditDiv.innerHTML = `
            <textarea class="form-control" id="edit-post-textarea">${ postContent.textContent }</textarea>
            <div class="d-flex justify-content-center my-2">
                <button id="edit-button" class="btn btn-primary mx-1">Edit</button>
                <button id="close-button" class="close-button btn btn-dark mx-1">Close</button>
            </div>
        `;
        postDiv.appendChild(postEditDiv);

        // Hide post content and datetime
        postElements.style.display = "none";

        // Edit and close buttons
        const editButton = postDiv.querySelector("#edit-button");
        const closeButton = postDiv.querySelector("#close-button");

        // Close button function (delete edit post block)
        closeButton.onclick = () => {
            document.getElementById("edit-post-div").remove();
            editMode = false;
            postElements.style.display = "block";
        };

        // Edit button function
        editButton.onclick = () => {
            // Edit post textarea with new content
            const documentEditTextarea = postDiv.querySelector("#edit-post-textarea");
            // New content
            const new_content = documentEditTextarea.value;
            // Make a request to change edit's content
            if (postContent.textContent !== new_content) {
                fetch(`edit-post/${postId}`, {
                    method: "PUT",
                    body: JSON.stringify({
                        post_content: new_content,
                    }),
                });
                // Change post content on page
                postContent.textContent = new_content;
            };
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
        button.innerHTML = isLiked ? likeIcon : unlikeIcon;
        
        // Update the button onclick event to toggle like/unlike functionality
        button.onclick = () => likeUnlike(!isLiked, postId, button);
    });
};
