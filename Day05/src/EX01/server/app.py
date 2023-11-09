import os
import mimetypes

from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.wrappers.response import Response


MUSIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static/music')

app: Flask = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


class Song:
    def __init__(self, name: str, filename: str) -> None:
        self.name: str = name.replace('_', ' ')
        self.files: list[tuple] = [(
            mimetypes.guess_type(
                os.path.join(MUSIC_FOLDER, filename)
            )[0],
            filename,
        )]

    def add_file(self, filename: str) -> None:
        self.files.append((
            mimetypes.guess_type(
                os.path.join(MUSIC_FOLDER, filename)
            )[0],
            filename,
        ))

    def __str__(self) -> str:
        return self.name + str(self.files)

    def __repr__(self) -> str:
        return self.name + str(self.files)


@app.route('/', methods=['POST', 'GET'])
def index() -> str | Response:
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file: FileStorage = request.files['file']
        if not file or not file.filename:
            flash('No selected file')
            return redirect(request.url)
        mime_type: str | None = mimetypes.guess_type(file.filename)[0]
        if mime_type and not mime_type.startswith('audio'):
            flash('Non-audio file detected')
            return redirect(request.url)
        filename: str = secure_filename(file.filename)
        file.save(os.path.join(MUSIC_FOLDER, filename))
        return redirect(request.url)
    # if request.method == 'GET'
    songs: list[Song] = []
    filenames: list[str] = os.listdir(MUSIC_FOLDER)
    files: dict[str, int] = {}
    # to avoid duplicating files with the same name
    for i in range(len(filenames)):
        if filenames[i] == '.gitkeep':
            continue
        filename = filenames[i].split('.')[0]
        if filename not in files:
            songs.append(Song(filename, filenames[i]))
            files[filename] = i
        else:
            songs[files[filename]].add_file(filenames[i])
    return render_template('index.html', songs=songs)


if __name__ == '__main__':
    app.run(port=8888, debug=True)
