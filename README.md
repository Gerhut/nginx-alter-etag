# nginx-alter-etag

This is a repository to investigate alter etag in nginx.

## Problem

When using nginx as a reverse proxy, and do some response replacement using
[ngx_http_sub_module](). There is an issue that when the replacement rule is
changed but the upstream response is not, etag of the response will not be
changed, and the browser cannot receive the fresh result with the newer
replacement.

## Design

- During proxy response, nginx appends a hardcoded **proxy etag** to `Etag`
  header field of the upstream response.
- During proxy request, nginx will deconstruct the `If-None-Match` header field
  to **upstream etag** and **proxy etag**.
    - If **proxy etag** matches the current **proxy etag**, proxy the
      **upstream etag** as `If-None-Match` header field to upstream.
    - If **proxy etag** does not matches the current **proxy rtag**, do not proxy
      the `If-None-Match` header field to upstream.

It may be implemented by [ngx_http_map_module]() or some Perl script.

I'll try map directive first. Success

[ngx_http_sub_module]: http://nginx.org/en/docs/http/ngx_http_sub_module.html
[ngx_http_map_module]: http://nginx.org/en/docs/http/ngx_http_map_module.html

## Run

    $ docker-compose up --build
