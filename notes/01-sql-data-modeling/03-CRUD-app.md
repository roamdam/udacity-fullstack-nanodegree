First CRUD application
======================

# Concepts

## CRUD

Every web application (the controllers within it ?) must allow the four 
following operations on the database.

- Create : insert new items into database after user action
- Read : fetch items from the database to send them to the views
- Update : update an existing item after user action
- Delete : delete items in the database

## MVC

See [this tutorial](https://realpython.com/the-model-view-controller-mvc-paradigm-summarized-with-legos/).

## AJAX

### Definition

Difference between synchronous requests and asynchronous. Synchronous means that
every action on the client side triggers a request and waits for a response from
the server, usually implying a page refresh.

AJAX (Asynchronous javascript and xml) allows asynchronous request, which is, thanks
to a javascript code handling user action, not waiting for the server response to
complete before doing other things. Using javascript allows to modify (from the
DOM) dynamically the content of the web page with the response from the server, 
without having to refresh it. That reduces latency and improve user experienc
(remember RIA = rich internet applications).

Historical technique is `XMLHttprequests`, but tends to be replaced by the more
effective and easy to handle `fetch` method in javascript.

- [Wikipedia](https://fr.wikipedia.org/wiki/Ajax_(informatique)) is quite thorough on the subject.

### Example

Fetch method is based on promises, that is a representation of the state of the
request made to the server. This is what allows not to wait for the answer to do
other things.

Instead, just define the expected behaviour *once the request has completed* (or
failed). This is done by chaining `.then(callback))` statements to fetch, that
will be triggered once the request has completed, without stopping the web server
altogether. See [MDN](https://developer.mozilla.org/fr/docs/Web/API/Fetch_API/Using_Fetch)
for detailed API.

```javascript
document.getElementById("add-item-form").onsubmit = function(e) {
    e.preventDefault()            // stop usual behaviour for a form submission
    fetch('/todos/create', {      // send a POST request to /todos/create route
        method: 'POST',
        body: JSON.stringify({    // specify the body of the POST request
            'text': document.getElementById("todo-text").value,
            'due-date': document.getElementById("todo-date").value
        }),
        headers: new Headers({    // specify content of the body
            'Content-Type': "application/json"
        })
    })
        .then(function(response) {
            // response.json() is a promise so actual 
            // conversion to json is made with another .then()
            return response.json() ;
        })
        // Once we got the answer from the server, we can start to update the DOM
        .then(function(response) {
            // Handle empty list message presence
            let empty_list_message = document.getElementById('empty-list-message'),
                todo_list = document.createElement("ul") ;
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
            let inner_text = `${response['text']}` ;
            if (response['due-date']) {
                inner_text += ` (${response['due-date']})` ;
            }
            const LiItem = document.createElement('li') ;
            LiItem.innerHTML = inner_text ;
            document.getElementById("todo-list").appendChild(LiItem) ;
        })
}
```

# Ressources

## Flask

- [Large applications](https://flask.palletsprojects.com/en/1.1.x/patterns/packages/)
- [Security in flask](https://flask.palletsprojects.com/en/1.1.x/security/)
- [Flask routes](https://hackersandslackers.com/flask-routes/)

## HTML

- [Forms](https://developer.mozilla.org/fr/docs/Web/HTML/Element/Form)
- [Form input](https://developer.mozilla.org/fr/docs/Web/HTML/Element/Input)

## HTTP

- [Methods](https://www.w3schools.com/tags/ref_httpmethods.asp)
