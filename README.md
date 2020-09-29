# Team Health Check voting app

Small flask application to record vote during Team Health session.

## How does it work

Anyone can create a room, they become admin of that room (uuid).
They can create a shortlink for that room.
They can delete the room whenever they want.
Rooms should will be purged a week after creation.

## TODO

- review room management
- export the result or easy copy paste to g doc
- allow admin to close a room
- use redis or db or something to allow multiple worker/instances
- For fun: add theme on client side

## Redis

Will not be using a password so make sure it's not available from the outside

```
docker run --name some-redis -d -v /docker/host/dir:/data redis redis-server --appendonly yes
```
