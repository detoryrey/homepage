const userId = 1;
const plannedBooksList = document.getElementById('plannedBooksList');
const readBooksList = document.getElementById('readBooksList');

function addBOOK(bookId, listType) {
    fetch('/add_book', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_id: userId, book_id: bookId, list_type: listType})
    })
        .then(res => res.json())
    .then(data => {
        if(data.success){
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = 'Book ID: ' + bookId;
            if(listType === 'planned') plannedBooksList.appendChild(li);
            else readBooksList.appendChild(li);
        }
    });
}