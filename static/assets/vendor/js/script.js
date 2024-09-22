// Jobs BookMark Toggle
document.getElementById('bookmarkToggle').addEventListener('click', function() {
    const iconOn = this.querySelector('.icon-on');
    const iconOff = this.querySelector('.icon-off');
    
    iconOn.classList.toggle('d-none');
    iconOff.classList.toggle('d-none');
});


