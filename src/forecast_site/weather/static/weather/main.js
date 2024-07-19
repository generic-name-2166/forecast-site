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
  const [left, right] = document.querySelectorAll(".weather-controls > button");
  const row = document.querySelector(".weather-row");
  left.addEventListener("click", () => {
    row.scrollLeft -= 100;
  });
  right.addEventListener("click", () => {
    row.scrollLeft += 100;
  });
}

function main() {
  const showPopup = saveCity();
  if (!showPopup) {
    const city = localStorage.getItem("city");
    // TODO
  }
  addScrollButtons();
}
 
main()
