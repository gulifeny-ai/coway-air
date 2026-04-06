// Coway-AIR 공통 JS (향후 확장용)
document.addEventListener('DOMContentLoaded', function () {
    // 현재 페이지에 해당하는 네비 활성화
    var path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function (link) {
        if (path.startsWith(link.getAttribute('href'))) {
            link.style.background = 'rgba(255,255,255,0.12)';
            link.style.color = '#fff';
        }
    });
});
