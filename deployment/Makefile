CONF_FILE = deploy.yaml

serve:
	python main.py

deploy:
	sky launch -c joblog $(CONF_FILE)

launch:
	sky launch -c joblog $(CONF_FILE)

exec:
	sky exec joblog $(CONF_FILE)
