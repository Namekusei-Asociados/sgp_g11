//add class active to navbar option
function getActiveNavOption(){
    const urlOptions = document.querySelectorAll("#side-bar-options .nav-item a")
    const activeSection = document.getElementById('active-section')?.getAttribute('data-value')

    urlOptions.forEach(e =>{
        if (e.getAttribute('data-section-active') === activeSection){
            e.classList.add('active')
        }
    })
}
getActiveNavOption()