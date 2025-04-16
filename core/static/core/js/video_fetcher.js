document.addEventListener('DOMContentLoaded', function () {
    const videosContainer = document.getElementById('videos-container');
    const loadMoreTrigger = document.getElementById('load-more-trigger');
    const loadingMessage = document.getElementById('loading-message');
    const nextPage = document.getElementById('next_page');

    let isLoading = false;

    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !isLoading) {
            loadMoreVideos(nextPage, videosContainer, loadingMessage);
        }
    }, { threshold: 0.5 });

    observer.observe(loadMoreTrigger);
});


async function loadMoreVideos(next_page_element, container, loading) {
    loading.style.display = 'block';
    const next_page_token = next_page_element.dataset.nextpage ?? null;

    const data = await fetchVideos(next_page_token);


    data.videos.forEach(video => {
        const videoHTML = `
    <div class="group w-full max-w-[360px]">
        <div class="relative aspect-video  mb-2 flex">
            <img src="${video.thumbnail}" alt="${video.title}"
                class="object-cover transition-transform duration-300 hover:scale-105 w-full rounded-sm">
            <div class="absolute bottom-1 right-1 bg-black/80 text-white text-xs px-1 py-0.5 rounded">
                ${video.duration}
            </div>
        </div>

        <div class="flex-1 min-w-0">
            <div class="flex justify-between ">
                <a href="/watch?v=${video.id}" class=" font-semibold line-clamp-2 hover:underline">${video.title}</a>
            </div>

            <a href="/channel/${video.channelTitle}" class="text-xs text-muted-foreground">${video.channelTitle}</a>

            <div class="text-xs text-muted-foreground">
                <span>${video.views} visualizacines </span>
            </div>
        </div>
    </div>`;

        container.insertAdjacentHTML('beforeend', videoHTML);
    });

    next_page_element.dataset.nextpage = data.next_page_token;

    loading.style.display = 'none';
}


async function fetchVideos(next_page_token) {
    const url = next_page_token ? `/list_videos?page=${next_page_token}` : `/list_videos`

    try {
        const data = await fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        }).then(response => response.json());

        return data;

    } catch (error) {
        return {};
    }
}