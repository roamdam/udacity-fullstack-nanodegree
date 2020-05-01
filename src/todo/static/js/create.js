function activate(e) {
    let card = document.getElementById('card') ;
    if (card) {
        card.remove() ;
    } else {
        let card = document.createElement('div'),
            children = e.target.childNodes ;
        card.id = 'card' ;
        for (let i = 0; i < children.length; i++) {
            const child = children[i].cloneNode(deep=true) ;
            card.appendChild(child) ;
        }
        document.getElementById('content-body').appendChild(card) ;
    }
}

function create_todo_item(response) {
    let todo_item = document.createElement('div'),
                todo_text = document.createElement('span'),
                todo_date = document.createElement('span');
    todo_item.className = 'list-item' ;
    todo_item.onclick = function(e) {activate(e)} ;

    todo_text.innerHTML = response['text'] ;
    todo_text.className = 'item-text' ;
    todo_item.appendChild(todo_text) ;

    if (response['due-date']) {
        todo_date.innerHTML = response['due-date'] ;
        todo_date.className = 'item-date' ;
        todo_item.appendChild(todo_date) ;
    }

    return todo_item ;
}


document.getElementById("add-item-form").onsubmit = function(e) {
    e.preventDefault() ;
    fetch('/todos/create', {
        method: 'POST',
        body: JSON.stringify({
            'text': document.getElementById("todo-text").value,
            'due-date': document.getElementById("todo-date").value
        }),
        headers: new Headers({
            'Content-Type': "application/json"
        })
    })
        .then(function(response) {
            // hide error message if it exists
            document.getElementById('error-container').style.display = 'none' ;
            return response ;
        })
        .then(function(response) {
            // response.json() is a promise so actual 
            // conversion to json is made with another .then()
            return response.json() ;
        })
        .then(function(response) {
            // Handle empty list message presence
            let empty_list_message = document.getElementById('empty-list-message'),
                todo_list = document.createElement("div") ;
            todo_list.id = 'todo-list' ;
            if (empty_list_message){
                let message_display = empty_list_message.style.display ;
                if (message_display !==  'none'){
                    document.getElementById("list-container").appendChild(todo_list) ;
                }
                empty_list_message.style.display = 'none';
            }
            return response ;
        })
        .then(function(response) {
            // Add a list item with json content
            todo_item = create_todo_item(response) ;
            document.getElementById("todo-list").appendChild(todo_item) ;
        })
        .then(function(response) {
            e.target.reset() ;
        })
        .catch(function(error) {
            alert('Something went wrong ! Please try again.') ;
        })
}
