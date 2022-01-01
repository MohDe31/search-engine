const axios = require('axios').default;
const cheerio = require('cheerio');
const path = require('path');
const url_tob64 = require('./image');

const { add_image, get_from_url } = require('./database');

const SUPPORTED_FILES = ['.png', '.jpg', '.jpeg', '.gif'];

const worldwildlife = 'https://www.worldwildlife.org/species/elephant';
const britannica = 'https://www.britannica.com/animal/elephant-mammal';
const thespruce = 'https://www.thespruce.com/pictures-of-ducks-4121960';


const URLs = [worldwildlife, britannica, thespruce];


const TEXT_TYPE  = 1;
const IMAGE_TYPE = 2;

async function searchImage(file) {
    const { name, path, type } = file;
    // TODO: Check for type

    const fileReader = new FileReader();
    fileReader.onload = async () => {
        // console.log(fileReader.result);
        const response = await fetch('http://127.0.0.1:5000', {
            method: 'POST',
            headers: { 
                'Content-Type': "application/json"
            },
            body: JSON.stringify({
                type: IMAGE_TYPE,
                content: fileReader.result.split('base64,')[1]
            })
        });

        const data = await response.json();

        if(data.success){
            const imageArray = data.data;
            addImages(imageArray);
        }
    }
    fileReader.readAsDataURL(file);
}

async function searchFor(value) {
    const response = await fetch('http://127.0.0.1:5000', {
        method: 'POST',
        headers: { 
            'Content-Type': "application/json"
        },
        body: JSON.stringify({
            type: TEXT_TYPE,
            content: value
        })
    });

    const results = await response.json();

    console.log(results);

    if(results.success)
    {
        addImages(results.data)
    }
}

// function searchFor(value) {

    
//     URLs.forEach(url => {
//         searchInLink(url);
//     });

//     async function searchInLink(link)
//     {
        
//         value = value.toLowerCase();


//         const result = await axios.get(link);

//         if (result.status == 200) {
//             const $ = cheerio.load(result.data);


//             const title = $('title').text().toLowerCase();

//             console.log(title);
//             /** @type Array<string> */
//             let images = depthSearch($('body')[0])

//             images = images.filter((value) => SUPPORTED_FILES.some((mime) => value.endsWith(mime))).map(val => [val, path.parse(val).name]);
            
//             let _db_res_obj = {};
//             (await get_from_url(link)).forEach((val) => {
//                 _db_res_obj[val.file_name] = "data:image/png;base64," + val.b64;
//             });

            
//             images = images.map(function(val) {
//                 if(!_db_res_obj[val[1]])
//                 {
//                     add_to_database(link, val);
//                     return val;
//                 }
//                 return [_db_res_obj[val[1]], val[1]];
//             });

//             //images_names = images.map((val) => path.parse(val).name);
//             //print(images_names)
            

//             // if searched value in the title
//             if (title.includes(value)) {
//                 addImages(images)
//                 return;
//             }

//             // search in paragraphs TODO:
//             //console.log($('body').html());

//             // search in images tags
//             images = images.filter(val => val[1].toLowerCase().includes(value));

//             addImages(images);
//         }

//     }
    

// }

async function add_to_database(link, [url, name])
{
    try{
        let b64 = await url_tob64(url);
        add_image(link, url, name, b64);

        console.log("Image Added");
    }catch(err){
        console.error(err);
    }
}

function depthSearch(parentNode) {
    let images = [];

    if (parentNode.type == 'tag') {
        if (parentNode.attribs.src)
            images.push(parentNode.attribs.src)


        for (let i = 0; i < parentNode.children.length; i += 1) {
            images = images.concat(depthSearch(parentNode.children[i]));
        }

    }


    return images;
}

