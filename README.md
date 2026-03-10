Build a Github repository which automatically sends an event (webhook) on the following
Github actions ("Push", "Pull Request", "Merge") to a registered endpoint, and store it to
MongoDB.

This github repo contains the code for registered endpoint.
This contains APIs handling 
> POST for Github actions ("Push", "Pull Request", "Merge") and storing them in mongodb database
> GET for fetching the stored data from mongodb database

There is another repo from where we get the request for storing the performed Github actions ("Push", "Pull Request", "Merge") 
Using webhook concept present in github where we just have to mention the api endpoint which is going to receive the data related 
to those actions.
