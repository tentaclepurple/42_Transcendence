# Endpoints

---
  ## User Reg, Login & Auth
---
### POST localhost:8000/auth/registration/

  Authorization required NO

    Body:
        {
            "username": "w",
            "email": "w@gmail.com",
            "password1": "popopopo0987",
            "password2": "popopopo0987"
        }
    
    Return:
        {
            "detail": "User registered successfully. Please log in."
        }

---
### POST localhost:8000/twofa/send-code/

  Authorization required NO

    Body:
        {
            "username": "w",
            "email": "w@gmail.com"
        }
    
    Return:
        Email sent. Use the code sent in the login process


---
### POST localhost:8000/auth/login/

  Authorization required NO

    Body:
        {
            "username": "w",
            "code": "791983",
            "password": "popopopo0987"
        }
    
    Return:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2OTgyNDQ5LCJpYXQiOjE3MTY5Nzg4NDksImp0aSI6ImRlMTJiZDY0NGY5NzRlYTY5MWI4N2RiNjczOGEzYzUyIiwidXNlcl9pZCI6OH0.xZ438bS7qxpSLnwmC3lpFIMq8ZP_ZTAJANtmLSNvrYE",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzA2NTI0OSwiaWF0IjoxNzE2OTc4ODQ5LCJqdGkiOiIwODdjY2I5YjI4NDU0ZGExODlmODIzMzI4MzZhYjJmOSIsInVzZXJfaWQiOjh9._iuC9Ifvi3b6SaS1f54yQeMa11gtzLeo3eWpWZOmxLc",
            "token_auth": "7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb"
        }

  Sets is_connected to true
  Deletes the 2fa code used
  Use token_auth from this point on:
  
    headers:
    Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

---
### POST localhost:8000/auth/logout/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
      {
          "detail": "Successfully logged out."
      }
Deletes token

---
### POST localhost:8000/api/token/refresh/

  Authorization required YES

    Headers:
         Bearer: Token <refresh token>

    Return:
      {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2OTgyNDQ5LCJpYXQiOjE3MTY5Nzg4NDksImp0aSI6ImRlMTJiZDY0NGY5NzRlYTY5MWI4N2RiNjczOGEzYzUyIiwidXNlcl9pZCI6OH0.xZ438bS7qxpSLnwmC3lpFIMq8ZP_ZTAJANtmLSNvrYE",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzA2NTI0OSwiaWF0IjoxNzE2OTc4ODQ5LCJqdGkiOiIwODdjY2I5YjI4NDU0ZGExODlmODIzMzI4MzZhYjJmOSIsInVzZXJfaWQiOjh9._iuC9Ifvi3b6SaS1f54yQeMa11gtzLeo3eWpWZOmxLc",
      }

---
 
  ## User Management
----
### POST localhost:8000/auth/password/change/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Body:
      {
          "new_password1": "popopopo1234",
          "new_password2": "popopopo1234"
      }

    Return:
      {
            "detail": "New password has been saved."
      }

---
### POST localhost:8000/users/update/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Body:
      {
          "username": "potxoloTheThird",
          "avatar": "/media/avatars/fary.png"
      }

    Return:
      {
            "username": "potxoloTheThird",
            "is_connected": true,
            "avatar": "/media/media/avatars/fary.png",
             "friends": [
                "jimenetz"
            ]
      }
---
### GET localhost:8000/users/user_list/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
      [
            {
                "username": "jimenetz",
                "is_connected": false,
                "avatar": "/media/avatars/default.png",
                "friends": [
                    "carmentxu",
                    "potxoloTheThird"
                ]
            },
            {
                "username": "manoli",
                "is_connected": false,
                "avatar": "/media/avatars/default.png",
                "friends": []
            },
            {
                "username": "potxoloTheThird",
                "is_connected": true,
                "avatar": "/media/media/avatars/fary.png",
                "friends": [
                    "jimenetz"
                ]
            }
        ]
---

### POST localhost:8000/users/add_friend/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Body:
      {
          "friend_username": "manoli"
      }

    Return:
      {
          "success": true,
          "message": "manoli added as friend."
      }

---
### POST localhost:8000/users/remove_friend/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Body:
      {
          "friend_username": "manoli"
      }

    Return:
      {
          "success": true,
          "message": "manoli added as friend."
      }
  ---
### GET localhost:8000/users/friend_list/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb


    Return:
      [
          {
              "username": "carmentxu",
              "is_connected": true,
              "avatar": "/media/avatars/default.png",
              "friends": [
                  "ramoncin"
              ]
          },
          {
              "username": "potxolo",
              "is_connected": true,
              "avatar": "/media/avatars/default.png",
              "friends": [
                  "ramoncin"
              ]
          }
      ]
---
  ## OAuth
---
### GET localhost:8000/oauth/authorize

  Authorization required NO

  Get 42 user data
  Creates a user in our db with 42 data (login, email, image)
  Ends with the user registered and logged in (is_connected, is_42 = True)


    Return:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2OTgyNDQ5LCJpYXQiOjE3MTY5Nzg4NDksImp0aSI6ImRlMTJiZDY0NGY5NzRlYTY5MWI4N2RiNjczOGEzYzUyIiwidXNlcl9pZCI6OH0.xZ438bS7qxpSLnwmC3lpFIMq8ZP_ZTAJANtmLSNvrYE",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzA2NTI0OSwiaWF0IjoxNzE2OTc4ODQ5LCJqdGkiOiIwODdjY2I5YjI4NDU0ZGExODlmODIzMzI4MzZhYjJmOSIsInVzZXJfaWQiOjh9._iuC9Ifvi3b6SaS1f54yQeMa11gtzLeo3eWpWZOmxLc",
            "token_auth": "7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb"
        }

---
  ## Chat
---
### POST localhost:8000/conversations/start/

  Authorization required YES
  Target user must be connected

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Body:
      {
          "username":"manoli" (target user)
      }

    Return:
      {
          "conversation_id": 4,
          "initiator": {
              "username": "jimenetz",
              "is_connected": true,
              "avatar": "/media/avatars/default.png",
              "friends": [
                  "carmentxu",
                  "potxoloTheThird"
              ]
          },
          "receiver": {
              "username": "manoli",
              "is_connected": true,
              "avatar": "/media/avatars/default.png",
              "friends": []
          }
      }
  ---
### GET localhost:8000/conversations/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
        [
            {
                "initiator": {
                    "username": "jimenetz",
                    "is_connected": false,
                    "avatar": "/media/avatars/default.png",
                    "friends": [
                        "carmentxu",
                        "potxoloTheThird"
                    ]
                },
                "receiver": {
                    "username": "manoli",
                    "is_connected": true,
                    "avatar": "/media/avatars/default.png",
                    "friends": []
                },
                "last_message": null
            }
        ]
  ---
  ### GET localhost:8000/conversations/<int:convo_id>/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
        {
            "initiator": {
                "username": "jimenetz",
                "is_connected": false,
                "avatar": "/media/avatars/default.png",
                "friends": [
                    "carmentxu",
                    "potxoloTheThird"
                ]
            },
            "receiver": {
                "username": "manoli",
                "is_connected": true,
                "avatar": "/media/avatars/default.png",
                "friends": []
            },
            "message_set": []
        }
  ---
  ### WEBSOCKET ws://localhost:8000/ws/chat/<int:convo_id>/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

  Connect to websocket
  Send/receive message
  ---