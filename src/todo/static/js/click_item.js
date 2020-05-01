function activate(list_item) {
    const active_item = document.getElementById().classList.contains('active') ;
    if (active_item) {
        list_item.classList.remove('active')
        console.log('deactivated item')
    } else {
        list_item.classList.add('active')
        console.log('activated item')
    }
}
