
document.addEventListener('DOMContentLoaded', async () => {

    const video_id = new URLSearchParams(document.location.search).get('v');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const like = document.getElementById('like');
    const dislike = document.getElementById('dislike');
    const user_comment = document.getElementById('user_comment');
    const user_comment_form = document.getElementById('user_comment_form');
    const user_comment_textarea = document.getElementById('user_comment');

    const comments_container = document.getElementById('comments_container');




    function autoGrow(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
    }
      
      // Usage:
      
      user_comment_textarea.addEventListener('input', () => autoGrow(user_comment_textarea));
      // Initialize on load
      autoGrow(user_comment_textarea);



    const updateButtonsInterface = (total_likes, total_dislikes, user_vote, to_update) => {

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

    const { total_likes, total_dislikes, user_vote } = await fetchVideoLikesDislike(video_id);

    updateButtonsInterface(total_likes, total_dislikes, user_vote);


    like.addEventListener("click", async (e) => {
        const { total_likes, total_dislikes, user_vote } = await LikeOrDislikeVideo(csrfToken, video_id)
        updateButtonsInterface(total_likes, total_dislikes, user_vote, like);
    });

    dislike.addEventListener("click", async (e) => {
        const { total_likes, total_dislikes, user_vote } = await LikeOrDislikeVideo(csrfToken, video_id, false)
        updateButtonsInterface(total_likes, total_dislikes, user_vote, dislike);
    });


    user_comment_form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const { success, data } = await commentVideo(csrfToken, video_id, user_comment.value);

        if (success) {
            const newElement = document.createElement('div');
            newElement.innerHTML = `
                <div class="flex w-full  p-2 justify-between gap-2">
                    <div class="avatar">
                    <div class="w-12 h-12 rounded-full">
                        <img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
                    </div>
                    </div>
                    <div class="w-full flex flex-col">
                    <span class="text-sm">@${data.user}</span>
                    <pre class="text-sm">${data.comment}</pre>
                    </div>
                </div>
                <div class="divider m-0 p-0"></div>
                `;

            comments_container.prepend(newElement);
        }
        user_comment_textarea.value = ''
        autoGrow(user_comment_textarea);
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
    const url = `/video/vote`

    try {
        const data = await fetch(url, {
            method: 'PUT', headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,  // Include CSRF token
            },
            body: JSON.stringify({ vote, video_id })
        }).then(response => response.json());

        return data;

    } catch (error) {
        return {};
    }
}



async function commentVideo(csrfToken, video_id, comment_content) {
    const url = `/comment/`

    try {

        const data = await fetch(url, {
            method: 'POST',
            body: JSON.stringify({ comment_content, video_id }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,  // Include CSRF token
            },
        }).then(response => response.json());


        return data;
    } catch (error) {
        return {};
    }
}