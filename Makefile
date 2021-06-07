dev:
	env DEPLOY_MODE="dev"
	env FLASK_APP="./app/main/main.py"
	flask run

prod:
	env DEPLOY_MODE="prod"
	env FLASK_APP="./app/main/main.py"
	flask run

tests:
	./venv/bin/python3 -c "import os; os.environ['DEPLOY_MODE'] = 'tests'"
	env DEPLOY_MODE="tests"
	python3 -m unittest app.test.model.user.UserModelTest