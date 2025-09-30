

function addBook(bookId, listType) {
    const userId = 1;
    fetch("/add_book", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({user_id: userId, book_id: bookId, list_type: listType})
    })
        .then(res => res.json())
        .then(data => console.log(data))
        .catch(err => console.error(err));
}
