var border_size = 40,
    list_background = document.getElementById("list-background"),
    delete_all = document.getElementById("delete-all"),
    insert_form = document.getElementById('add-item-form'),
    list_items = document.getElementsByClassName('list-item')
    items_date = document.getElementsByClassName('item-date') ;

function resize() {
    list_background.style.height = window.innerHeight - 2*border_size - delete_all.offsetHeight - insert_form.offsetHeight ;
}

function position_date() {
    let item_style = window.getComputedStyle(list_items[1]) ;

    let right_margin = parseInt(item_style.marginRight),
        right_padding = parseInt(item_style.paddingRight) ;

    for (i = 0; i < items_date.length; i++) {
        items_date[i].style.right = right_margin + right_padding
    } 
}

function onclick_items() {
    for (let i = 0; i < list_items.length; i++) {
        const list_item = list_items[i] ;
        list_item.onclick = function(e) {activate(e)} ;
        
    }
}


// position_date()
resize() ;
onclick_items() ;

window.onresize = function() {
    // position_date()
    resize() ;
}
