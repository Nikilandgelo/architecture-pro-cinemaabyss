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
	@kubectl create namespace $(NAMESPACE) --dry-run=client -o yaml | kubectl apply -f -
	@kubectl label namespace $(NAMESPACE) istio-injection=enabled --overwrite
	@echo "$$CI_SECRET_VALUES_PER_ENVIRONMENT" > values-secrets.yaml
	@helm upgrade --install $(RELEASE) . -f values-configmaps.yaml -f values-secrets.yaml -n $(NAMESPACE)
	@rm -f values-secrets.yaml
