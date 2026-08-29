## Задание 1 ✅
1. Спроектируйте to be архитектуру КиноБездны, разделив всю систему на отдельные домены и организовав
интеграционное взаимодействие и единую точку вызова сервисов. Результат представьте в виде
контейнерной диаграммы в нотации С4. Добавьте ссылку на файл в этот шаблон
[ссылка на файл](./schemas/Containers.puml)


## Задание 2 ✅
### 1. Proxy
Команда КиноБездны уже выделила сервис метаданных о фильмах movies и вам необходимо реализовать
бесшовный переход с применением паттерна Strangler Fig в части реализации прокси-сервиса (API Gateway),
с помощью которого можно будет постепенно переключать траффик, используя фиче-флаг.

Реализуйте сервис на любом языке программирования в ./src/microservices/proxy.
Конфигурация для запуска сервиса через docker-compose уже добавлена

- После реализации запустите postman тесты - они все должны быть зеленые.
- Отправьте запросы к API Gateway:
- Протестируйте постепенный переход, изменив переменную окружения MOVIES_MIGRATION_PERCENT в файле 
docker-compose.yml.

### 2. Kafka
Вам как архитектуру нужно также проверить гипотезу насколько просто реализовать применение Kafka в
данной архитектуре.

Для этого нужно сделать MVP сервис events, который будет при вызове API создавать и сам же читать
сообщения в топике Kafka.

- Разработайте сервис на любом языке программирования с consumer'ами и producer'ами.
- Реализуйте простой API, при вызове которого будут создаваться события User/Payment/Movie и
обрабатываться внутри сервиса с записью в лог

Приложите скриншот тестов и скриншот состояния топиков Kafka http://localhost:8090
![Tests](./images/terminal.png)
![Kafka Topics](./images/kafbat.png)


## Задание 3 ✅
Команда начала переезд в Kubernetes для лучшего масштабирования и повышения надежности. 
Вам, как архитектору осталось самое сложное:
 - реализовать CI/CD для сборки прокси сервиса
 - реализовать необходимые конфигурационные файлы для переключения трафика.

### CI/CD
В папке .github/workflows доработайте деплой новых сервисов proxy и events в docker-build-push.yml,
чтобы api-tests при сборке отрабатывали корректно при отправке коммита в вашу новую ветку.

Как только сборка отработает и в github registry появятся ваши образы, можно переходить к блоку
настройки Kubernetes. Успешным результатом данного шага является "зеленая" сборка и "зеленые" тесты.


### Proxy в Kubernetes
#### Шаг 1
Для деплоя в kubernetes необходимо залогиниться в docker registry Github'а.

#### Шаг 2
  Доработайте src/kubernetes/event-service.yaml и src/kubernetes/proxy-service.yaml
  - Необходимо создать Deployment и Service 
  - Доработайте ingress.yaml, чтобы можно было с помощью тестов проверить создание событий
  - Откройте логи event-service и сделайте скриншот обработки событий

![Events](./images/events.png)

#### Шаг 3
Добавьте сюда скриншота вывода при вызове https://cinemaabyss.example.com/api/movies и
скриншот вывода event-service после вызова тестов.
- ![Movies Output](./images/movies_output.png)
- ![Tests Output](./images/tests_output.png)
- ![Tests Output Console](./images/tests_output_console.png)


## Задание 4
Для простоты дальнейшего обновления и развертывания вам как архитектуру необходимо так же
реализовать helm-чарты для прокси-сервиса и проверить работу.

Для этого:
1. Перейдите в директорию helm и отредактируйте файл values.yaml

```yaml
# Proxy service configuration
proxyService:
  enabled: true
  image:
    repository: ghcr.io/db-exp/cinemaabysstest/proxy-service
    tag: latest
    pullPolicy: Always
  replicas: 1
  resources:
    limits:
      cpu: 300m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi
  service:
    port: 80
    targetPort: 8000
    type: ClusterIP
```

- Вместо ghcr.io/db-exp/cinemaabysstest/proxy-service напишите свой путь до образа для всех сервисов
- для imagePullSecret проставьте свое значение (скопируйте из конфигурации kubernetes)
  ```yaml
  imagePullSecrets:
      dockerconfigjson: ewoJImF1dGhzIjogewoJCSJnaGNyLmlvIjogewoJCQkiYXV0aCI6ICJaR0l0Wlhod09tZG9jRjl2UTJocVZIa3dhMWhKVDIxWmFVZHJOV2hRUW10aFVXbFZSbTVaTjJRMFNYUjRZMWM9IgoJCX0KCX0sCgkiY3JlZHNTdG9yZSI6ICJkZXNrdG9wIiwKCSJjdXJyZW50Q29udGV4dCI6ICJkZXNrdG9wLWxpbnV4IiwKCSJwbHVnaW5zIjogewoJCSIteC1jbGktaGludHMiOiB7CgkJCSJlbmFibGVkIjogInRydWUiCgkJfQoJfSwKCSJmZWF0dXJlcyI6IHsKCQkiaG9va3MiOiAidHJ1ZSIKCX0KfQ==
  ```

2. В папке ./templates/services заполните шаблоны для proxy-service.yaml и events-service.yaml
(опирайтесь на свою kubernetes конфигурацию - смысл helm'а сделать шаблоны для быстрого обновления и установки)

```yaml
template:
    metadata:
      labels:
        app: proxy-service
    spec:
      containers:
       Тут ваша конфигурация
```

3. Проверьте установку. Сначала удалим установку руками

```bash
kubectl delete all --all -n cinemaabyss
kubectl delete  namespace cinemaabyss
```
Запустите 
```bash
helm install cinemaabyss .\src\kubernetes\helm --namespace cinemaabyss --create-namespace
```
Если в процессе будет ошибка
```code
[2025-04-08 21:43:38,780] ERROR Fatal error during KafkaServer startup. Prepare to shutdown (kafka.server.KafkaServer)
kafka.common.InconsistentClusterIdException: The Cluster ID OkOjGPrdRimp8nkFohYkCw doesn't match stored clusterId Some(sbkcoiSiQV2h_mQpwy05zQ) in meta.properties. The broker is trying to join the wrong cluster. Configured zookeeper.connect may be wrong.
```

Проверьте развертывание:
```bash
kubectl get pods -n cinemaabyss
minikube tunnel
```

Потом вызовите 
https://cinemaabyss.example.com/api/movies
и приложите скриншот развертывания helm и вывода https://cinemaabyss.example.com/api/movies


# Задание 5
Компания планирует активно развиваться и для повышения надежности, безопасности, реализации сетевых
паттернов типа Circuit Breaker и канареечного деплоя вам как архитектору необходимо развернуть istio
и настроить circuit breaker для monolith и movies сервисов.

```bash
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

helm install istio-base istio/base -n istio-system --set defaultRevision=default --create-namespace
helm install istio-ingressgateway istio/gateway -n istio-system
helm install istiod istio/istiod -n istio-system --wait

helm install cinemaabyss .\src\kubernetes\helm --namespace cinemaabyss --create-namespace

kubectl label namespace cinemaabyss istio-injection=enabled --overwrite

kubectl get namespace -L istio-injection

kubectl apply -f .\src\kubernetes\circuit-breaker-config.yaml -n cinemaabyss

```

Тестирование

# fortio
```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.25/samples/httpbin/sample-client/fortio-deploy.yaml
-n cinemaabyss
```

# Get the fortio pod name
```bash
FORTIO_POD=$(kubectl get pod -n cinemaabyss | grep fortio | awk '{print $1}')

kubectl exec -n cinemaabyss $FORTIO_POD -c fortio -- fortio load -c 50 -qps 0 -n 500 -loglevel Warning
http://movies-service:8081/api/movies
```

Например,
```bash
kubectl exec -n cinemaabyss fortio-deploy-b6757cbbb-7c9qg  -c fortio -- fortio load -c 50 -qps 0 -n
500 -loglevel Warning http://movies-service:8081/api/movies
```

Вывод будет типа такого
```bash
IP addresses distribution:
10.106.113.46:8081: 421
Code 200 : 79 (15.8 %)
Code 500 : 22 (4.4 %)
Code 503 : 399 (79.8 %)
```

Можно еще проверить статистику
```bash
kubectl exec -n cinemaabyss fortio-deploy-b6757cbbb-7c9qg -c istio-proxy -- pilot-agent request GET stats | grep movies-service | grep pending
```

И там смотрим
```bash
cluster.outbound|8081||movies-service.cinemaabyss.svc.cluster.local;.upstream_rq_pending_total: 311 - столько раз срабатывал circuit breaker
You can see 21 for the upstream_rq_pending_overflow value which means 21 calls so far have been flagged for circuit breaking.
```

Приложите скриншот работы circuit breaker'а
