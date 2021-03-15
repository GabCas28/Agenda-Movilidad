const titleInput = document.querySelector('input[name=title]');
const slugInput = document.querySelector('input[name=slug]');

const slugify = (val) =>{
    return val.toString().toLowerCase().trim()
        .replace(/&/g, '-and-')     //replace '&' with '-and-'
        .replace(/\s/g,'-')    //replace spaces, non word chards and dahses with a single dash
        .replace(/[\W-]+/g,'-')    //replace spaces, non word chards and dahses with a single dash
};
if (titleInput){
    titleInput.addEventListener('keyup', (e) =>{
        slugInput.setAttribute('value', slugify(titleInput.value))
    })

}