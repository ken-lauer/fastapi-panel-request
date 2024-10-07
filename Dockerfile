FROM condaforge/miniforge3:latest


RUN useradd \
        --create-home \
        --shell /bin/bash \
        --uid 1000 \
        user

USER user

WORKDIR /install
COPY env.yaml .

RUN mamba env create -f env.yaml
SHELL ["conda", "run", "--no-capture-output", "-n", "panel", "/bin/bash", "-c"]

RUN conda list

WORKDIR /app
COPY entrypoint.sh /app

COPY src /app/src

CMD ["conda", "run", "--no-capture-output", "-n", "panel", "/bin/bash", "/app/entrypoint.sh"]
