FROM --platform=linux/amd64 mambaorg/micromamba:1.5.3

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml

RUN micromamba install -y -n base -f /tmp/environment.yml && \
micromamba clean --all --yes

WORKDIR /app

COPY --chown=$MAMBA_USER:$MAMBA_USER parma_mining /app/parma_mining

ENV FIREBASE_ADMINSDK_CERTIFICATE=$FIREBASE_ADMINSDK_CERTIFICATE
ENV PDL_API_KEY=$PDL_API_KEY
ENV PDL_API_VERSION=$PDL_API_VERSION
ENV PDL_BASE_URL=$PDL_BASE_URL

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]
CMD ["uvicorn", "parma_mining.peopledatalabs.api:app", "--host", "0.0.0.0", "--port", "8080"]