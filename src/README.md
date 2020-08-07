# Project Usage

---

To run the project on your machine, you can follow the steps given below:

* Create a virtual environment and activate it

* Clone the project

* Run the project using python manage.py runserver
---

# PHOTO API BASE URL

All endpoints generate from the base url given below:

* `url: /api/photos/`

---

# AUTHENTICATION 

 JWT Authentication is required to access authenticated endpoints.
 
---

# AUTHENTICATION ENDPOINTS

* Obtain Access and Refresh Token:

       
            URL: /api/token/
            METHOD: POST
            Request Body:{
                "username": <your_username>,
                "password": <your_password>
            }
            Example Response:{
                "refresh": <str>,
                "access": <str>
            }
          
* Refresh Token:

       
            URL: /api/token/refresh/
            METHOD: POST
            Request Body:{
                "refresh": <your_refresh_token>
            }
            Example Response:{
                "access": <str>
            }
           
# AUTHENTICATION HEADER
   As JWT authentication is required to access authenticated endpoints. You should provide 
   authentication header in the following format in your requests:
   ### Authorization: JWT <your_access_token_here>
   


# Supported API Endpoints

- List All Photos:

    *  ```
        URL: /all/
        METHOD: GET
        AUTHENTICATED : False
        SORT ASC: /?ordering=published_date
        SORT DESC: /?ordering=-published_date
        Filter User: /?search=<username>
        Example Response :
            {
                "count": 2,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "user": {
                            "id": 1,
                            "username": "testuser"
                        },
                        "image": "http://localhost:9002/media/user-uploaded-photos/testuser/11218556_1_ba59naA.jpeg",
                        "caption": "Hello world",
                        "is_draft": true,
                        "published_date": "2020-08-06"
                    },
                    {
                        "user": {
                            "id": 1,
                            "username": "testuer"
                        },
                        "image": "http://localhost:9002/media/user-uploaded-photos/testuser/11218556_1_cUALxDQ.jpeg",
                        "caption": "Frontend Photo",
                        "is_draft": false,
                        "published_date": "2020-08-06"
                    }       
                ]
            }

        ```

- User Photos List (My Photos):
    *  ```
        URL: /user/
        AUTHENTICATED: True
        METHOD: GET
        Example Response :
            {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "user": {
                            "id": 1,
                            "username": "testuser"
                        },
                        "image": "http://localhost:9002/media/user-uploaded-photos/testuser/11218556_1_ba59naA.jpeg",
                        "caption": "Hello world",
                        "is_draft": false,
                        "published_date": "2020-08-06"
                    }
                ]
            }

        ```
 
 - User Draft Photos:
    *  ```
        URL: /user/drafts/
        AUTHENTICATED: True
        METHOD: GET
        Example Response :
            {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "user": {
                            "id": 1,
                            "username": "testuser"
                        },
                        "image": "http://localhost:9002/media/user-uploaded-photos/testuser/11218556_1_ba59naA.jpeg",
                        "caption": "Hello world",
                        "is_draft": true,
                        "published_date": "2020-08-06"
                    }
                ]
            }

       ```
 - Create Photo:
    *  ```
        URL: /create/
        AUTHENTICATED: True
        METHOD: POST
        Request Body:
            {
                "image": <image file>,
                "captions": <str>,
                "is_draft": <bool> 
            }


        Example Response :              
                    {
                        "user": {
                            "id": 1,
                            "username": "testuser"
                        },
                        "image": "http://localhost:9002/media/user-uploaded-photos/testuser/11218556_1_ba59naA.jpeg",
                        "caption": "Hello world",
                        "is_draft": true,
                        "published_date": "2020-08-06"
                    }



        ```
  
 - Update Photo Caption:
    *  ```
        URL: /update/<int:pk>/
        AUTHENTICATED: True
        METHOD: PUT,PATCH
        Request Body:
            {
               "captions": <str>
            }


        Example Response :              
                    {
                        "caption": "New Caption",  
                    }
        
        ```
        
- Delete Photo:
    *  ```
        URL: /delete/<int:pk>/
        AUTHENTICATED: True
        METHOD: DELETE
        Example Response :              
                    {
                        
                    }
       Response Code: 204_NO_CONTENT
        ```
---

# ERRORS AND MESSAGES

| RESPONSE   | STATUS CODE | Message |
| ------------- | ------------- | ------------- |
| SUCCESS  | HTTP_200_OK   | Request Processed Successfully  |
| CREATED  | HTTP_201_CREATED  | Object Created Successfully  |
| NO CONTENT | HTTP_204_NO_CONTENT  | Object Deleted Successfully |
| BAD REQUEST | HTTP_400_BAD_REQUEST | Request was in an invalid format. Check that your params have been properly encoded in the POST body and that your content     is UTF8 encoded |
| UNAUTHORIZED | HTTP_401_UNAUTHORIZED | Request made was unauthenticated.Make sure to use your authentication credentials to request the resource |
| FORBIDDEN | HTTP_403_FORBIDDEN | Request permission not allowed |
| NOT FOUND | HTTP_404_NOT_FOUND | Looked up resource could not be found |


# TEST APPLICATION DEPLOYED LIVE
  The web application has been deployed live on Digital Ocean. It can be accessed from the following IP address:
  
    http://188.166.234.28/
  
  - Test User Credentials: 
  
         Username : hmlet
         Password : testuser
        

If you have any questions or need admin access, kindly email me at the following email address:
ammar88ammar@gmail.com
  
