FROM python:3.8
COPY . /app
RUN pip install requests && pip install pandas
WORKDIR /app
CMD [ "python", "./period_profit_gotham_asset.py" ]