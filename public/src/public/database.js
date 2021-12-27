const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database("./database.db");



db.serialize(function () {
    db.run("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, website TEXT NOT NULL, file_url TEXT NOT NULL, file_name TEXT NOT NULL, b64 TEXT NOT NULL UNIQUE);");
});





function add_image(link, url, name, b64)
{
    db.run(`INSERT INTO images (website, file_url, file_name, b64) VALUES("${link}", "${url}", "${name}", "${b64}");`, (res, err) => {
        if(err)console.error(err);
        
    });
}

async function get_from_url(url)
{
    return new Promise((resolve, reject) => {
        db.all(`SELECT * FROM images WHERE website = "${url}";`, function(err, rows) {
            resolve(rows);
        })
    });
}

async function get_all_images()
{
    return new Promise((resolve, reject) => {
        db.serialize(function(){
            db.all("SELECT * FROM images", function(err, rows) {
                resolve(rows);
            });
        });
    });
}


module.exports = {add_image, get_all_images, get_from_url};