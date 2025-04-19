
document.addEventListener('DOMContentLoaded', async () => {

    const video_id = new URLSearchParams(document.location.search).get('v');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const user_comment_form = document.getElementById('user_comment_form');
    const user_comment_textarea = document.getElementById('user_comment');

    const comments_container = document.getElementById('comments_container');


    textAreaAutoGrow(user_comment_textarea);


    user_comment_textarea.addEventListener('input', () => textAreaAutoGrow(user_comment_textarea));


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
        textAreaAutoGrow(user_comment_textarea);
    });
})


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

const textAreaAutoGrow = (textarea) => {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}
