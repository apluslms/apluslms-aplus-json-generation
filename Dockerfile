FROM apluslms/service-base:python3-1.5

ARG BRANCH=milestone0.3

RUN :\
    # apluslms-roman
    && mkdir /roman \
    && cd /roman \
    && git clone https://github.com/apluslms/roman.git .\
    && git checkout $BRANCH \
    && rm -rf .git \
    # install requirements and the yaml_validator package, remove unrequired locales and tests
    && pip3 install -r requirements_build.txt \
    &&  ./scripts/build_wheels.sh \
    &&  pip3 install `find dist -name "apluslms_yamlidator-*.whl"` \
    && find /usr/local/lib/python* -type d -regex '.*/locale/[a-z_A-Z]+' -not -regex '.*/\(en\|fi\|sv\)' -print0 | xargs -0 rm -rf \
    && find /usr/local/lib/python* -type d -name 'tests' -print0 | xargs -0 rm -rf


RUN mkdir -p /app/schemas
# RUN mkdir /schemas

COPY schemas/. /app/schemas/
COPY . /app/


ENTRYPOINT ["python3", "/app/main.py"]
