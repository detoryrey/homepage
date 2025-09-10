  document.addEventListener("DOMContentLoaded", function() {
    const toastElList = [].slice.call(document.querySelectorAll('.toast'))
    toastElList.forEach(function(toastEl) {
      const toast = new bootstrap.Toast(toastEl, { delay: 4000 }) // 4 сек
      toast.show()
    })
  })