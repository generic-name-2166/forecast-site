function storageAvailable(type) {
  let storage;
  try {
    // I don't even know what it wants from me here
    //@ts-expect-error
    storage = window[type];
    const x = "__storage_test__";
    storage.setItem(x, x);
    storage.removeItem(x);
    return true;
  } catch (e) {
    return (
      e instanceof DOMException &&
      (e.name === "QuotaExceededError" ||
        e.name === "NS_ERROR_DOM_QUOTA_REACHED") &&
      // acknowledge QuotaExceededError only if there's something already stored
      storage &&
      storage.length !== 0
    );
  }
}

function saveCity() {
  const url = new URL(window.location.href);
  const city = url.searchParams.get("city");

  if (city === null || !storageAvailable("localStorage")) {
    return true;
  }

  window.addEventListener("DOMContentLoaded", () => {
    localStorage.setItem("city", city);
  });
  return false;
}

function addScrollButtons() {
  const leftButtons = document.querySelectorAll(".weather-controls > .left");
  const rightButtons = document.querySelectorAll(".weather-controls > .right");
  const rows = document.querySelectorAll(".weather-controls .weather-row");
  
  for (let i = 0; i < leftButtons.length; i++) {
    const left = leftButtons[i];
    const right = rightButtons[i];
    const row = rows[i];
    left.addEventListener("click", () => {
      row.scrollLeft -= 100;
    });
    right.addEventListener("click", () => {
      row.scrollLeft += 100;
    });
  }
}

function showSelectedDay() {
  let previous = 0;
  const days = document.querySelectorAll(".selected-day");
  const options = document.querySelectorAll(".selected-select");

  const toggle = (index) => () => {
    days[previous].classList.toggle("hidden");
    days[index].classList.toggle("hidden");
    previous = index;
  };

  for (let i = 0; i < options.length; i++) {
    options[i].addEventListener("click", toggle(i));
  }

  days[previous]?.classList.toggle("hidden");
}

function main() {
  const showPopup = saveCity();
  if (!showPopup) {
    const city = localStorage.getItem("city");
    // TODO
  }
  addScrollButtons();
  showSelectedDay();
}
 
main()
