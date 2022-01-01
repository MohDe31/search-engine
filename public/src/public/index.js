let searchBar;

/** @type Element */
let imageContainer;
let inputContainer;

window.onload = () => {
    document.querySelector("#search_btn").onclick = search;
    document.querySelector("#image_btn").onclick = openImage;

    inputContainer = document.querySelector("#openimg");

    inputContainer.onchange = (e)=> {
        const file = e.target.files[0];
        imageContainer.innerHTML = '';
        e.target.value = "";
        searchImage(file);
    }

    searchBar = document.querySelector('#search_');

    imageContainer = document.querySelector('#img_container');


    searchBar.onkeypress = (e)=>{
        
        // On click enter
        if(e.keyCode == 13)
        {
            search();
        }
    }
}

function openImage()
{
    inputContainer.click();
}

function search()
{
    let val = searchBar.value;

    imageContainer.innerHTML = '';

    if(!val) return;

    searchFor(val);
}

function createImage(ele)
{
    let { src, name, type } = ele;

    let img_div = document.createElement('div');
    img_div.classList.add('img_div');
    
    let img = document.createElement('img');
    if(type == "B64") img.src = "data:image/png;base64," + src
    else img.src = src;
    img.onerror = 'alert("cannot load")';
    img.classList.add('res-img');

    let img_name = document.createElement('p');
    img_name.classList.add('img-name');
    img_name.innerText = name;

    let tbg = document.createElement('div');
    tbg.classList.add('tbg');

    let overlay = document.createElement('div');
    overlay.classList.add('overlay');

    img_div.appendChild(img);

    tbg.appendChild(img_name);

    img_div.appendChild(tbg);
    img_div.appendChild(overlay);

    return img_div;
}

function addImages(images)
{
    const imagesEles = images.map(createImage);
    
    imagesEles.map((ele) => imageContainer.appendChild(ele));
    
}