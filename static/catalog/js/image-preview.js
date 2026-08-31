(function () {
  function addPreview(input) {
    var file = input.files && input.files[0];
    if (!file || !file.type.match(/^image\/(jpeg|png|webp)$/)) {
      return;
    }
    var preview = input.parentNode.querySelector(".live-image-preview");
    if (!preview) {
      preview = document.createElement("img");
      preview.className = "live-image-preview";
      preview.style.cssText = "display:block;width:96px;height:72px;object-fit:cover;border-radius:6px;margin-top:8px";
      input.parentNode.appendChild(preview);
    }
    var reader = new FileReader();
    reader.onload = function () { preview.src = reader.result; };
    reader.readAsDataURL(file);
  }

  document.addEventListener("change", function (event) {
    if (event.target.matches("input[type=file]")) {
      addPreview(event.target);
    }
  });
}());