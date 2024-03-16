const http = require('http');
const fs = require('fs');

const port = 80;
const page = fs.readFileSync("index.html").toString();

const mime = {
    html: 'text/html',
    txt: 'text/plain',
    css: 'text/css',
    gif: 'image/gif',
    jpg: 'image/jpeg',
    png: 'image/png',
    svg: 'image/svg+xml',
    js: 'application/javascript'
};

function make_folder_if_not_exists(folder) {
    if(!fs.existsSync(folder)) {
        fs.mkdirSync(folder + "/");
    }
}

make_folder_if_not_exists("./data");

function qual_or_playoff_folder_name(is_qual) {
    return is_qual ? "qual" : "playoff";
}

function log_data(data) {
    console.log("writing: " + data);
    make_folder_if_not_exists("./data/" + data["team_number"])
    const iq = qual_or_playoff_folder_name(data["is_qual"]);
    make_folder_if_not_exists("./data/" + data["team_number"] + "/" + iq);
    fs.writeFile("./data/" + data["team_number"] + "/" + iq + "/" + data["match_number"] + ".txt", JSON.stringify(data), {flag: "w+"}, (err) => {
        console.error(err);
    });
}

const server = http.createServer((req, res) => {
    if(req.method == "POST") {
        var body = '';

        req.on('data', function (data) {
            body += data;

            // Too much POST data, kill the connection!
            // 1e6 === 1 * Math.pow(10, 6) === 1 * 1000000 ~~~ 1MB
            if (body.length > 1e6)
                request.connection.destroy();
        });

        req.on('end', () => {
            var post = JSON.parse(body);
            log_data(post);
            res.end();
        });
    } else if(req.method == "GET") {
        res.statusCode = 200;
        if(req.url == "/") {
            res.setHeader('Content-Type', 'text/html');
            res.end(page);
        } else if(req.url.startsWith("/resources/")) {
            var tmp = req.url.split(".");
            res.setHeader('Content-Type', mime[tmp[tmp.length - 1]]);
            var s = fs.createReadStream("." + req.url);
            s.on('open', () => {
                s.pipe(res);
            }); // this is probably inefficient? idk
        }
    }
});

server.listen(port);