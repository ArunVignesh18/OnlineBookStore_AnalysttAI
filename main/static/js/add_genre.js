function removeGenre(genreId) {
  fetch("/remove_genre/" + genreId + "/")
    .then((response) => {
      if (response.ok) {
        return response.json(); // Parse the response as JSON
      } else {
        throw new Error("Failed to remove the genre."); // Throw an error to trigger the catch block
      }
    })
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else {
        location.reload();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert(error);
    });
}
