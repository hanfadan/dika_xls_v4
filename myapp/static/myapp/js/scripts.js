function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

document.querySelectorAll('.has-submenu > a').forEach(item => {
    item.addEventListener('click', function(e) {
        e.preventDefault();
        this.parentElement.classList.toggle('open');
    });
});
