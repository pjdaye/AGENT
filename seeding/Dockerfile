FROM aist-python

USER root

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY mongo_seeder.py /app/
COPY forms.json /app/

CMD python3 seed_form_expert_data.py
