FROM apluslms/service-base:python3-1.5

ARG BRANCH=milestone0.3

RUN :\
    # create user and aplus_json dir
    && adduser --system --disabled-password --gecos "A+ json generation,,," --home /srv/aplus_json --ingroup nogroup aplus_json \
    && chown aplus_json.nogroup /srv/aplus_json \
    && mkdir /srv/aplus_json/schemas \
    # apluslms-roman
    && mkdir /srv/roman \
    && cd /srv/roman \
    && git clone https://github.com/apluslms/roman.git .\
    && git checkout $BRANCH \
    && rm -rf .git \
    # install requirements and the yaml_validator package, remove unrequired locales and tests
    && pip3 install -r requirements_build.txt \
    &&  ./scripts/build_wheels.sh \
    &&  pip3 install `find dist -name "apluslms_yamlidator-*.whl"` \
    && find /usr/local/lib/python* -type d -regex '.*/locale/[a-z_A-Z]+' -not -regex '.*/\(en\|fi\|sv\)' -print0 | xargs -0 rm -rf \
    && find /usr/local/lib/python* -type d -name 'tests' -print0 | xargs -0 rm -rf

COPY main.py course.py parser.py utils.py /srv/aplus_json/
COPY schemas/. /srv/aplus_json/schemas/

WORKDIR /srv/aplus_json/
