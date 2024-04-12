document.addEventListener('DOMContentLoaded', () => {

    const followButton = document.getElementById('profile-button-follow-unfollow');
    const usernameProfile = document.getElementById('profile_username').innerHTML;

    fetch(`${usernameProfile}/is-following`)
    .then(response => response.json())
    .then(result => {
        const currentUserUsername = document.getElementById('user-username').innerHTML;
        
        followButton.innerHTML = result.is_following ? 'Unfollow' : 'Follow';
        followButton.onclick = () => followUnfollow(followButton, result.is_following, currentUserUsername);
    });
});

function followUnfollow(button, isFollowing, follower) {
    const usernameProfile = document.getElementById('profile_username').innerHTML;
    const method = isFollowing ? 'DELETE' : 'POST';
    // Change button text to the opposite
    button.innerHTML = isFollowing ? "Follow" : "Unfollow";
    
    fetch(`${usernameProfile}/is-following`, {
        method: method,
        body: JSON.stringify({
            follower: follower,
            followed_user: usernameProfile,
        }),
    });

    button.onclick = () => followUnfollow(button, !isFollowing, follower);
};