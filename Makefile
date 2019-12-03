.PHONY: deploy

deploy:
	nvm use
	yarn build
	git commit -am "production build for release"
	git push
	# fullrelease
