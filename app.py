from flask import Flask, json, render_template, request;
from pathlib import Path;
app = Flask(__name__);

# create data directory
data = Path("data/");
data.mkdir(parents=True, exist_ok=True);

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html');

@app.route('/post', methods=['POST'])
def post():
    res = request.form.to_dict(flat=False); # flat is needed to handle the ARRAY VALUES

    # remove all the arrays that only have 1 value
    for k in res:
        if (k not in ('attempted_notes', "shot_locations")):
            res[k] = res[k][0];
            # if (res[k].isnumeric()):
            #     res[k] = int(res[k]);
            # elif res[k] == "on":
            #     res[k] = True;
    print("saving:", res);

    team_folder = data / res["team_number"] / ("qual" if res["is_qual"] == "on" else "playoff");
    team_folder.mkdir(parents=True, exist_ok=True);
    data_file = team_folder / (res["match_number"] + ".txt");
    with data_file.open("w", encoding ="utf-8") as f:
        f.write(json.dumps(res));

    
    return res

if __name__ == "__main__":
    app.run(debug=True)
