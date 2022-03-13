# Games I Played
A web application written in [Python](https://www.python.org/) by using [Django](https://www.djangoproject.com/) framework.

## Purpose
This web application is created as an assignment for SWE 573 course in Boğaziçi University. It allows the owner to share his/her games publicly.

## Development
Required Python package information is provided in _requirements.txt_ file. So, you can install dependencies like this:

```bash
pip install -r requirements.txt
```

After that, the application can be run on development server like this:

```bash
python manage.py runserver
```

## Deployment
The application is currently hosted on AWS. It was deployed by using Elastic Beanstalk service. However, it has been deployed manually, so, there is no CI/CD process right now.

The latest deployed version of the application can be seen on [http://gamesiplayed.us-east-1.elasticbeanstalk.com/](http://gamesiplayed.us-east-1.elasticbeanstalk.com/) address.

## Resources and References
[https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)

[https://realpython.com/deploying-a-django-app-and-postgresql-to-aws-elastic-beanstalk/](https://realpython.com/deploying-a-django-app-and-postgresql-to-aws-elastic-beanstalk/)

[https://startbootstrap.com/template/bare](https://startbootstrap.com/template/bare)

[https://howlongtobeat.com/](https://howlongtobeat.com/)

[https://www.wikidata.org/](https://www.wikidata.org/)
