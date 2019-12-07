import pathlib
from datetime import datetime
from flask import Flask


_ROOT_DIR = pathlib.Path(__file__).absolute().parent.parent
_INDEX_HTML = '''
<html>
    <head></head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''
_USER_PAGE_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {thoughts}
        </table>
    </body>
</html>
'''
_USER_THOUGHT_HTML = '''
<tr>
    <td>{ts}</td>
    <td>{thought}</td>
</tr>
'''

app = Flask(__name__)


def run_webserver(address, data_dir):
    data_path = pathlib.Path(data_dir)
    @app.route('/')
    def handle_index():
        users_html = []
        for user_dir in data_path.iterdir():
            users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
        return _INDEX_HTML.format(users='\n'.join(users_html))

    @app.route('/users/<user_id>')
    def handle_user(user_id):
        thoughts = []
        print(user_id)
        data_user_dir_path = data_path / user_id
        for thought_file in data_user_dir_path.iterdir():
            user_thought = _USER_THOUGHT_HTML.format(
                ts=get_date_from_filename(file=thought_file),
                thought=thought_file.read_text())
            thoughts.append(user_thought)
        return _USER_PAGE_HTML.format(user_id=data_user_dir_path.name,
                                      thoughts='\n'.join(thoughts))
    host, port = address
    app.run(host=host, port=port)


def get_date_from_filename(file):
    ts = datetime.strptime(file.stem, '%Y-%m-%d_%H-%M-%S')
    return ts.strftime('%Y-%m-%d %H:%M:%S')


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        addr_arr = argv[1].split(':')
        run_webserver((addr_arr[0], int(addr_arr[1])), argv[2])
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
