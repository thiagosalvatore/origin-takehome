# Pull in the from the official nginx image.
FROM nginx:1.9

# Optionally set a maintainer name to let people know who made this image.
MAINTAINER Thiago Salvatore <thiago.salvatore@gmail.com>

# We'll need curl within the nginx image.
RUN apt-get update && apt-get install -y --no-install-recommends curl \
      && rm -rf /var/lib/apt/lists/*

# Delete the default welcome to nginx page.
RUN rm /usr/share/nginx/html/*

# Copy over the custom nginx and default configs.
RUN rm /etc/nginx/conf.d/*
COPY configs/nginx.conf /etc/nginx/nginx.conf
COPY configs/default.conf /etc/nginx/conf.d/default.conf

RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# Allow us to customize the entrypoint of the image.
COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

# Start nginx in the foreground to play nicely with Docker.
CMD ["nginx", "-g", "daemon off;"]