# Install Langfuse for langchain

Devchain is currently using [langfuse](https://langfuse.com/) for tracing and monitoring. It is an **Open source LLM engineering Platform** similar to Langsmith.

## Install

Follow these instructions to self-host langfuse via docker.

1. Install Postgresql.
```sh
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql
```
You can find the instructions on the [website](https://www.postgresql.org/download/linux/ubuntu/).

2. Launch it, it is better to run it as a server.
```sh
sudo systemctl start postgresql
```

```sh
sudo systemctl stop postgresql
```

3. Configure the server by modifying this file : /etc/postgresql/16/main/postgresql.conf.
Set listen adresses to *.
```sh
listen_addresses = '*'
```

Configure to use md5.
```sh
sudo sed -i '/^host/s/ident/md5/' /etc/postgresql/16/main/pg_hba.conf
sudo sed -i '/^local/s/peer/trust/' /etc/postgresql/16/main/pg_hba.conf
echo "host all all 0.0.0.0/0 md5" | sudo tee -a /etc/postgresql/16/main/pg_hba.conf
```

Pass through the firewall.
```sh
sudo ufw allow 5432/tcp
```

4. Add a new line in '/etc/postgresql/16/main/pg_hba.conf'.
```sh
host    all             all             0.0.0.0/0               md5 to pg_hba.conf
```

5. Connect to the database server and change the password.
```sh
sudo -u postgres psql
ALTER USER postgres PASSWORD '<password>';
```

5. Create the Postgres database,  you can use [db.sh](./db.sh)

6. Launch the docker image. Be careful, you need to access the localhost from the docker container.
Use the [launch.sh](./launch.sh) script.

## Useful link

https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql-linux/