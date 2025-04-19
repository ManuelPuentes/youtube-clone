document.addEventListener('DOMContentLoaded', async () => {

    const video_id = new URLSearchParams(document.location.search).get('v');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const like = document.getElementById('like');
    const dislike = document.getElementById('dislike');

    const { total_likes, total_dislikes, user_vote } = await fetchVideoLikesDislike(video_id);

    updateLikeDislikeInterface(total_likes, total_dislikes, user_vote);

    like.addEventListener("click", async (e) => {
        const { total_likes, total_dislikes, user_vote } = await LikeOrDislikeVideo(csrfToken, video_id)
        updateLikeDislikeInterface(total_likes, total_dislikes, user_vote, like);
    });

    dislike.addEventListener("click", async (e) => {
        const { total_likes, total_dislikes, user_vote } = await LikeOrDislikeVideo(csrfToken, video_id, false)
        updateLikeDislikeInterface(total_likes, total_dislikes, user_vote, dislike);
    });

})

async function fetchVideoLikesDislike(video_id) {
    const url = `/video/vote?v=${video_id}`

    try {
        const data = await fetch(url).then(response => response.json());
        return data;

    } catch (error) {
        return {};
    }
}

async function LikeOrDislikeVideo(csrfToken, video_id, vote = true,) {
    const url = `/video/vote/`

    try {
        const data = await fetch(url, {
            method: 'post', headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,  // Include CSRF token
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ vote, video_id }),

        }).then(response => response.json());

        return data;

    } catch (error) {
        return {};
    }
}

const updateLikeDislikeInterface = (total_likes, total_dislikes, user_vote, to_update) => {

    if ((total_dislikes == undefined) || (total_dislikes == undefined)) return;

    if (to_update) to_update.classList.toggle('btn-secondary')

    like.innerText = `${total_likes} me gusta`;
    dislike.innerText = `${total_dislikes} no me gusta`;

    if (user_vote == null) return;

    if (user_vote) {
        like.classList.add('btn-secondary');
        dislike.classList.remove('btn-secondary');

    } else {
        dislike.classList.add('btn-secondary');
        like.classList.remove('btn-secondary');
    }

}

