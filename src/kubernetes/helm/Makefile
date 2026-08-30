RELEASE := cinemaabyss-release
NAMESPACE := cinemaabyss-helm

define CI_SECRET_VALUES_PER_ENVIRONMENT
secrets:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres_password
    POSTGRES_DB: cinemaabyss
endef
export CI_SECRET_VALUES_PER_ENVIRONMENT

deploy:
	@echo "$$CI_SECRET_VALUES_PER_ENVIRONMENT" > values-secrets.yaml
	@helm upgrade --install $(RELEASE) . -f values-configmaps.yaml -f values-secrets.yaml -n $(NAMESPACE) --create-namespace
	@rm -f values-secrets.yaml
