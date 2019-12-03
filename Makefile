.PHONY: deploy

deploy:
	nvm use
	yarn build
	fullrelease
