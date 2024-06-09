docker run --name langfuse --add-host host.docker.internal:host-gateway \
    -e DATABASE_URL=postgresql://postgres:password@host.docker.internal:5432/langfuse_db\
    -e NEXTAUTH_URL=http://0.0.0.0:3000 \
    -e NEXTAUTH_SECRET=mysecret \
    -e SALT=mysalt \
    -p 3000:3000 \
    -a STDOUT \
    ghcr.io/langfuse/langfuse:latest


# Add host    all             all             0.0.0.0/0               md5 to pg_hba.conf , and listen=*