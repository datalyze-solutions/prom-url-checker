FROM python:3-alpine

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    USER_NAME="server" \
    USER_ID=1001

RUN addgroup --gid ${USER_ID} ${USER_NAME} && \
    adduser --uid ${USER_ID} --disabled-password --ingroup ${USER_NAME} --gecos "KKI Analyst" ${USER_NAME} && \
    pip install flit

ADD ./ /src

USER ${USER_NAME}
ENV PATH="/home/${USER_NAME}/.local/bin:${PATH}"
RUN flit -f /src/pyproject.toml install --deps production

CMD ["prom-url-checker"]