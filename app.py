import logging
from flask import Flask, json, render_template, request, abort, json;
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
        if (k not in ('attempted_notes', "shot_locations_auton", "shot_locations_teleop")):
            if ("on" in res[k]):
                res[k] = "on"
            else:
                res[k] = res[k][0];
            # if (res[k].isnumeric()):
            #     res[k] = int(res[k]);
            # elif res[k] == "on":
            #     res[k] = True;
    app.logger.info("GOT RESPONSE from [" + request.remote_addr + "] | Team Number: " + res["team_number"] + ", Match Number: " + res["match_number"]);

    if (int(res["autoNotesScored"]) > int(res["autoNotesAttempted"])):
        return json.dumps({"message": "Auton Notes Scored > Auton Notes Attempted! This is impossible"}), 400

    if (int(res["teleNotesScored"]) > int(res["teleNotesAttempted"])):
        return json.dumps({"message": "Teleop Notes Scored > Teleop Notes Attempted! This is impossible"}), 400

    team_folder = data / res["team_number"] / ("qual" if res["is_qual"] == "on" else "playoff");
    team_folder.mkdir(parents=True, exist_ok=True);
    data_file = team_folder / (res["match_number"] + ".txt");
    if data_file.exists():
        return json.dumps({"message": "This submission already exists!"}), 400
    with data_file.open("w", encoding ="utf-8") as f:
        f.write(json.dumps(res));
        return json.dumps({"message": "Success"}), 200

    return json.dumps({"message": "Internal Server Error"}), 500

    

if __name__ == "__main__":

    app.run(debug=False)
else:
    # we are running wtih Gunicorn
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

