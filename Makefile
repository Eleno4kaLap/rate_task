up:
	@docker-compose -f docker-compose.yml up -d
	@docker images -q -f dangling=true | xargs docker rmi -f

up-build:
	@docker-compose -f docker-compose.yml up -d --build
	@docker images -q -f dangling=true | xargs docker rmi -f

down:
	@docker-compose -f docker-compose.yml down

shell:
	@docker-compose -f docker-compose.yml exec django python manage.py shell

# If the first argument is "test"...
ifeq (test,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "test"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
test:
	@docker-compose -f docker-compose.yml run -e PYTHONDONTWRITEBYTECODE=1 --rm django python3 manage.py test $(RUN_ARGS) --settings=config.settings