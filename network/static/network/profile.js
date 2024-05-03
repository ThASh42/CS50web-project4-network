document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.getElementById('profile-button-follow-unfollow');
    const currentUserUsername = document.getElementById('user-username').innerHTML;

    // isFollowing is defined in the HTML template (profile.html)
    followButton.innerHTML = isFollowing ? 'Unfollow' : 'Follow';
    followButton.onclick = () => followUnfollow(followButton, isFollowing, currentUserUsername);
});

function followUnfollow(button, isFollowing, follower) {
    const usernameProfile = document.getElementById('profile_username').innerHTML;
    const method = isFollowing ? 'DELETE' : 'POST';
    
    fetch(`${usernameProfile}/follow-unfollow`, {
        method: method,
        body: JSON.stringify({
            follower: follower,
            followed_user: usernameProfile,
        }),
    }).then(() => {
        // Change button functionality to the opposite
        button.innerHTML = isFollowing ? "Follow" : "Unfollow";
        button.onclick = () => followUnfollow(button, !isFollowing, follower);
    });
};