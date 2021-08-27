// 카메라 연동
const video = document.getElementById('video')

function starVideo() {
    navigator.getUserMedia(
        { video: {} },
        stream => video.srcObject = stream,
        err => console.error(err)
    )
}

starVideo()