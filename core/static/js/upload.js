document.addEventListener('DOMContentLoaded', () => {

    const form_id = document.getElementById('id');
    const form_title = document.getElementById('title');
    const form_thumbnail = document.getElementById('thumbnail');

    const video_title = document.getElementById('video_title');
    const video_thumbnail = document.getElementById('video_thumbnail');


    form_title.addEventListener("input", function (e) {
        video_title.innerText = e.target.value;
    });

    form_thumbnail.addEventListener("change", function (e) {
        const url = e.target.value;

        if (isvalidImageUrl(url)) {
            video_thumbnail.src = url;
        } else {
            video_thumbnail.src = ''
        }
    });




})


const isvalidImageUrl = (url) => {
    const regex = /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\/\w.-]*)*\/?\.(jpe?g|png|gif|webp|bmp|svg|ico)(\?.*)?$/i;
    return regex.test(url);
}