.PHONY: deploy
PATH := .:$(PATH)

deploy:
	bash -l -c 'nvm exec stable yarn build'
	git commit -am "production build for release"
	git push
	fullrelease

develop:
	bash -l -c 'nvm exec stable yarn start'
