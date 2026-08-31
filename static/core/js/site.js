(function () {
  var toggle = document.getElementById("menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      nav.classList.toggle("hidden", expanded);
    });
  }
  var images = Array.prototype.slice.call(document.querySelectorAll(".gallery-image"));
  var thumbs = Array.prototype.slice.call(document.querySelectorAll(".gallery-thumb"));
  thumbs.forEach(function (thumb) { thumb.addEventListener("click", function () { var index = Number(thumb.dataset.index); images.forEach(function (image, imageIndex) { image.classList.toggle("hidden", imageIndex !== index); }); thumbs.forEach(function (button, buttonIndex) { button.classList.toggle("is-selected", buttonIndex === index); }); }); });
  var main = document.getElementById("gallery-main");
  if (main && images.length > 1) { var startX = 0; main.addEventListener("touchstart", function (event) { startX = event.touches[0].clientX; }, { passive: true }); main.addEventListener("touchend", function (event) { var delta = event.changedTouches[0].clientX - startX; if (Math.abs(delta) < 40) return; var current = images.findIndex(function (image) { return !image.classList.contains("hidden"); }); var next = (current + (delta < 0 ? 1 : images.length - 1)) % images.length; thumbs[next].click(); }, { passive: true }); }
}());