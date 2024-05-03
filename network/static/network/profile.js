document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.getElementById('profile-button-follow-unfollow');
    const userElement = document.getElementById('user-username');

    if (userElement) {
        const currentUserUsername = userElement.textContent;
        // isFollowing is defined in the HTML template (profile.html)
        followButton.textContent = isFollowing ? 'Unfollow' : 'Follow';
        followButton.onclick = () => followUnfollow(followButton, isFollowing, currentUserUsername);
    };
});

function followUnfollow(button, isFollowing, follower) {
    const usernameProfile = document.getElementById('profile_username').innerHTML;
    const method = isFollowing ? 'DELETE' : 'POST';
    
    fetch(`${usernameProfile}/follow-unfollow`, {
        method: method,
        body: JSON.stringify({
            follower: follower,
        }),
    }).then(() => {
        // Change button functionality to the opposite
        button.innerHTML = isFollowing ? "Follow" : "Unfollow";
        button.onclick = () => followUnfollow(button, !isFollowing, follower);
    });
};