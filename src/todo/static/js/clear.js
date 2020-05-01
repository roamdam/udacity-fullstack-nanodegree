function remove(node) {
    const parent = node.parentNode ;
    while (parent.hasChildNodes()) {
        parent.removeChild(parent.firstChild) ;
    }
}


document.getElementById('delete-all').onsubmit = function(e) {
    e.preventDefault() ;
    fetch('/todos/clear', {
        method: 'POST'
    })
        .then(function(response) {
            if (!response.ok || response.status !== 200) {
                throw `Something went wrong : ${response.status}` ; 
            }
        })
        .then(function(response) {
            // hide error message if it exists
            document.getElementById('error-container').style.display = 'none' ;
        })
        .then(function(response) {
            // remove list ul element from tree
            const todo_list = document.getElementById('todo-list') ;
            if (todo_list) {
                remove(todo_list) ;
            }
        }) 
        .then(function(response) {
            let empty_list_message = document.getElementById('empty-list-message') ;
            // display empty message if it exists, create it otherwise
            if (empty_list_message){
                empty_list_message.style.display === 'block' ;
            } else {
                empty_list_message = document.createElement('div') ;
                empty_list_message.id = 'empty-list-message' ;
                empty_list_message.innerHTML = 'No items yet ! Add your first.' ;
                document.getElementById('list-container').appendChild(empty_list_message) ;
            }
        })
        .catch(function(error) {
            // Display error message in case of failure
            document.getElementById('error-container').style.display = 'block' ;
            console.log(error) ;
        })
}
