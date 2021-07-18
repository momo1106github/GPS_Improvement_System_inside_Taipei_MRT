# GPS_Improvement_System_inside_Taipei_MRT

## deploy

```
docker image build -t gpsimprov .
heroku container:push web
heroku container:release web
```