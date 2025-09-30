

function removeBook(bookId) {
  fetch('/remove_book', {
    method: 'POST',
    headers: {'Content-Type': 'application/json',},
    body: JSON.stringify({ book_id: bookId }),
  })
  .then(response => {
    if (response.ok) {location.reload();
    }
  })
  .catch(error => console.error('Error:', error));
}