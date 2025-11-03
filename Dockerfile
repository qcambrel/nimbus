FROM mambaorg/micromamba:latest

COPY environment.yml .

RUN micromamba create --name earth --file environment.yml && \
    micromamba clean --all --yes

ENV ENV_NAME=earth

COPY app.py .
COPY observations.yml .
COPY features ./features
COPY metrics ./metrics
COPY plotting ./plotting
COPY processing ./processing
COPY utils/ ./utils
COPY video ./video

CMD ["streamlit", "run", "app.py"]