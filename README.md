# GPS_Improvement_System_inside_Taipei_MRT

## Info

This is a college undergraduate research project contributed by
謝心默 and
張翔文

## What Are We Doing
[Introduction](https://momo1106github.github.io/GPS_Improvement_System_inside_Taipei_MRT/)

[google_docs link](https://docs.google.com/presentation/d/1AcaNFsT5V_fUxMzoXNRQDlywe_yVKwAkQQhU3umuwLE/edit?usp=sharing)

## Flow Chart

[gitmind flow chart](https://gitmind.com/app/flowchart/6542855934)


## deploy

```
docker image build -t gpsimprov .
heroku container:push web
heroku container:release web
```
