FROM ubuntu:22.04

# Add arguments for UID and GID
ARG UID=1000
ARG GID=1000
ENV HOME=/home/appuser

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-venv \
    curl \
    wget \
    fonts-nanum \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${GID} appuser && \
    useradd -u ${UID} -g appuser -m -s /bin/bash appuser

# 커널 디렉토리 환경 변수 설정 및 커널 디렉토리 생성
ENV KERNEL_ROOT_DIR=${HOME}/data

RUN mkdir -p ${KERNEL_ROOT_DIR} && chown -R appuser:appuser ${KERNEL_ROOT_DIR}

WORKDIR ${HOME}

USER appuser

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    && bash miniconda.sh -b -p ${HOME}/conda \
    && rm miniconda.sh

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${HOME}/poetry python3 -

ENV PATH="${HOME}/conda/bin:${PATH}"
ENV PATH="${HOME}/poetry/bin:${PATH}"
ENV PATH="${HOME}/.local/bin:${PATH}"

COPY --chown=appuser:appuser environment.yml ${HOME}/
RUN conda env create -f ${HOME}/environment.yml -n jarvis-ipybox && conda init bash

COPY --chown=appuser:appuser pyproject.toml ${HOME}/
RUN poetry config virtualenvs.create false
RUN conda run -n jarvis-ipybox poetry install --only main

# 커널 관리 스크립트 추가
COPY --chown=appuser:appuser custom_kernel_manager.py ${HOME}/

# 서버 실행 스크립트 추가
COPY --chown=appuser:appuser server.sh ${HOME}/
RUN chmod +x ${HOME}/server.sh

COPY --chown=appuser:appuser jarvis_ipybox/modinfo.py /app/jarvis_ipybox/

WORKDIR /app

CMD ["/bin/bash", "-c", "source ${HOME}/conda/etc/profile.d/conda.sh && conda activate jarvis-ipybox && ${HOME}/server.sh"]
