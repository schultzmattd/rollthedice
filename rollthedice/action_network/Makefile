clean:
	rm -rf build build.zip
	rm -rf __pycache__

fetch-dependencies:
	mkdir -p bin/

	# Get chromedriver
	# curl -SL https://chromedriver.storage.googleapis.com/2.43/chromedriver_linux64.zip > chromedriver.zip
	curl -SL https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip > chromedriver.zip
	unzip chromedriver.zip -d bin/

	# Get Headless-chrome
	curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-55/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
	unzip headless-chromium.zip -d bin/

	# Clean
	rm headless-chromium.zip chromedriver.zip

docker-build:
	mkdir -p src/rollthedice/action_network
	cp ../__init__.py src/rollthedice/
	cp __init__.py src/rollthedice/action_network/
	cp action_network_daemon.py src/rollthedice/action_network/
	cp utilities.py src/rollthedice/action_network/
	# Doesn't look like src/ is copied into the docker image, just mounted, so this should be fine
	cp .action src/rollthedice/action_network/

	docker-compose build

docker-run:
	docker-compose run lambda rollthedice.action_network.action_network_daemon.poll_loop

build-lambda-package: clean fetch-dependencies
	mkdir build
	cp -r src build/.
	cp -r bin build/.
	cp -r lib build/.
	pip install -r requirements.txt -t build/lib/.
	cd build; zip -9qr build.zip .
	cp build/build.zip .
	rm -rf build