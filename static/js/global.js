//function showModal(event, imageSrc) {
//    event.preventDefault();  // 기본 동작 차단
//
//    var modal = document.getElementById("myModal");
//    var modalImg = document.getElementById("modalImage");
//
//    modalImg.src = imageSrc;
//    modal.style.display = "block";
//
//    // 모달 창 바깥 영역 클릭 시 닫기
//    window.onclick = function(event) {
//        if (event.target == modal) {
//            modal.style.display = "none";
//        }
//    }
//}

document.addEventListener('DOMContentLoaded', (event) => {
    // 모든 뉴스 이미지에 이벤트 리스너 추가
    document.querySelectorAll('.news-image').forEach(image => {
        image.addEventListener('click', function() {
            showModal(this.src);
        });
    });

    // 모달 창 클릭 시 닫기
    document.querySelector('.modal').addEventListener('click', function() {
        this.style.display = 'none';
    });
});

function showModal(imageSrc) {
    var modal = document.querySelector('.modal');
    var modalContent = document.querySelector('.modal-content');
    // 모달에 이미지 삽입
    modalContent.innerHTML = '<img src="' + imageSrc + '" alt="News Image">';
    // 모달 창을 표시
    modal.style.display = 'flex';
}