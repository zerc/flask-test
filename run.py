#!venv/bin/python
# coding: utf-8
import project
import users

if __name__ == '__main__':
    project.db.create_all()  # for test only
    project.app.run(host='0.0.0.0', port=8000)
