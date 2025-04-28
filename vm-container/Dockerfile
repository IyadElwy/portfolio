FROM python:3.12-bookworm

RUN ["pip", "install", "fastapi[standard]", "pandas", "requests", "psycopg2"]

WORKDIR /app
COPY ./api ./api
RUN ["mkdir", "/appdata"]
WORKDIR /appdata
COPY ./movies_command_line_app.py .
WORKDIR /app/api
ENTRYPOINT ["python3", "/app/api/run.py"]

RUN ["useradd", "-m", "-d", "/home/narrator", "narrator"]
RUN ["mkdir", "/home/narrator/bin"]
RUN ["sh", "-c", "echo 'export PATH=$HOME/bin' | tee -a /home/narrator/.bashrc"]

RUN ["cp", "/bin/rbash", "/home/narrator/bin"]
RUN ["cp", "/bin/ls", "/home/narrator/bin"]
RUN ["cp", "/bin/cat", "/home/narrator/bin"]
RUN ["cp", "/bin/grep", "/home/narrator/bin"]
RUN ["cp", "/bin/head", "/home/narrator/bin"]
RUN ["cp", "/bin/tail", "/home/narrator/bin"]
RUN ["cp", "/bin/wc", "/home/narrator/bin"]
RUN ["cp", "/bin/pwd", "/home/narrator/bin"]
RUN ["cp", "/bin/awk", "/home/narrator/bin"]
RUN ["cp", "/bin/sed", "/home/narrator/bin"]
RUN ["cp", "/bin/stat", "/home/narrator/bin"]
RUN ["cp", "/bin/whoami", "/home/narrator/bin/whoami"]

RUN ["usermod", "-s", "/home/narrator/bin/rbash", "narrator"]
COPY ./movies.sh /home/narrator/bin/movies
RUN ["chmod", "+x", "/home/narrator/bin/movies"]

RUN ["chmod", "-R", "555", "/home/narrator/bin"]
RUN ["chmod", "555", "/home/narrator/.bash_logout"]
RUN ["chmod", "555", "/home/narrator/.bashrc"]
RUN ["chmod", "555", "/home/narrator/.profile"]

USER narrator:narrator

COPY ./CheckMeOut /home/narrator/CheckMeOut

WORKDIR /home/narrator
