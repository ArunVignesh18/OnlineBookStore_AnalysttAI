const fetchBooks = async () => {
  const title = document.getElementById("titleInput").value.trim();
  const author = document.getElementById("authorInput").value.trim();
  const ratings = document.getElementById("ratingsSelect").value;
  const priceMin = document.getElementById("priceMinInput").value.trim();
  const priceMax = document.getElementById("priceMaxInput").value.trim();
  const startDate = document.getElementById("startDateInput").value;
  const endDate = document.getElementById("endDateInput").value;
  const genreSelect = document.getElementById("genreSelect");
  const genres = genreSelect.options[genreSelect.selectedIndex].value;

  try {
    const response = await axios.get("/api/book_list/");
    const books = response.data;

    const filteredBooks = books.filter((book) => {
      let isValid = true;

      if (title && !book.title.toLowerCase().includes(title.toLowerCase())) {
        isValid = false;
      }

      if (author && !book.author.toLowerCase().includes(author.toLowerCase())) {
        isValid = false;
      }

      if (ratings && book.customer_ratings < ratings) {
        isValid = false;
      }

      if (priceMin && parseFloat(book.price) < parseFloat(priceMin)) {
        isValid = false;
      }

      if (priceMax && parseFloat(book.price) > parseFloat(priceMax)) {
        isValid = false;
      }

      if (startDate && book.publication_date < startDate) {
        isValid = false;
      }

      if (endDate && book.publication_date > endDate) {
        isValid = false;
      }

      if (
        genres.length > 0 &&
        !book.genres.some((genre) => genres.includes(genre.id.toString()))
      ) {
        isValid = false;
      }

      return isValid;
    });

    renderBookCards(filteredBooks);
  } catch (error) {
    console.error(error);
  }
};

const renderBookCards = (books) => {
  const bookCardsContainer = document.getElementById("bookCardsContainer");
  bookCardsContainer.innerHTML = "";

  let rowContainer = document.createElement("div");
  rowContainer.classList.add("row");

  books.forEach((book) => {
    const card = document.createElement("div");
    card.classList.add("card", "mb-4", "col-md-3");

    const cardHead = document.createElement("div");
    cardHead.classList.add("card-header");
    card.appendChild(cardHead);

    const title = document.createElement("h5");
    title.classList.add("card-title");
    title.textContent = book.title;
    cardHead.appendChild(title);

    const author = document.createElement("p");
    author.classList.add("card-text");
    author.textContent = `- ${book.author}`;
    cardHead.appendChild(author);

    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body");
    card.appendChild(cardBody);

    const cardImg = document.createElement("div");
    cardImg.classList.add("card-image-container");
    cardBody.appendChild(cardImg);

    const image = document.createElement("img");
    image.classList.add("card-img-top", "cardImg");
    image.src = book.cover_image;
    image.alt = book.title;
    cardImg.appendChild(image);

    const cardDetail = document.createElement("div");
    cardDetail.classList.add("card-details");
    cardBody.appendChild(cardDetail);

    const ratings = document.createElement("p");
    ratings.classList.add("card-text");
    ratings.textContent = `Ratings: ${book.customer_ratings}`;
    cardDetail.appendChild(ratings);

    const price = document.createElement("p");
    price.classList.add("card-text");
    price.textContent = `Price: \u20B9${book.price}`;
    cardDetail.appendChild(price);

    const cardFoot = document.createElement("div");
    cardFoot.classList.add("card-footer");
    card.appendChild(cardFoot);

    const viewButton = document.createElement("a");
    viewButton.classList.add("btn", "btn-primary", "mr-2", "card-button");
    viewButton.href = `/book/${book.id}/`;
    viewButton.textContent = "View Book";
    cardFoot.appendChild(viewButton);

    if (isAuthenticated) {
      const removeButton = document.createElement("a");
      removeButton.classList.add("btn", "btn-primary", "mr-2", "card-button");
      removeButton.id = "removeButton";
      removeButton.href = `/removeBook/${book.id}/`;
      removeButton.textContent = "Remove Book";
      cardFoot.appendChild(removeButton);
    } else {
      const addToCartButton = document.createElement("a");
      addToCartButton.classList.add("btn", "btn-primary", "card-button");
      addToCartButton.href = `/add_to_cart/${book.id}/`;
      addToCartButton.textContent = "Add to Cart";
      cardFoot.appendChild(addToCartButton);
    }

    rowContainer.appendChild(card);
    bookCardsContainer.appendChild(rowContainer);
  });
};

const searchForm = document.getElementById("searchForm");
searchForm.addEventListener("submit", function (event) {
  event.preventDefault();
  fetchBooks();
});

searchButton.removeEventListener("click", fetchBooks);

fetchBooks();
