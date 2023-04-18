const titleInput = document.querySelector("input[name=title]");
const slugInput = document.querySelector("input[name=slug]");

const slugify = (val) => {
  return val
    .toString()
    .toLowerCase()
    .trim()
    .replace(/&/g, "-and-") //replace '&' with '-and-'
    .replace(/\s/g, "-") // replace blank spaces with a single dash
    .replace(/[\W-]+/g, "-"); // replace non word chars and dashes with a single dash
};
if (titleInput) {
  titleInput.addEventListener("keyup", (e) => {
    slugInput.setAttribute("value", slugify(titleInput.value));
  });
}
