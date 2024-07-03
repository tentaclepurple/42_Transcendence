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
	(
		Para subir image: ?
	 	curl -X post <url> -F avatar=@<path>
	)
    
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

  Authorization required NO

    Body:
      {
          "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3NTg0OTQyLCJpYXQiOjE3MTc1ODQzMTAsImp0aSI6IjQyYzM3YmVjZTA2OTRjMTk4YzdmNzk5N2VjOGQzZjk4IiwidXNlcl9pZCI6N30.9GaPZ9bfO7e2cKeu8gwCi9SNjJqK3pSNuJ03JTqrUvc"
      }

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
		(
		Para subir image: ?
	 	curl -X post <url> -F avatar=@<path>
		)


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

### GET localhost:8000/users/profile/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
      [
            {
				"id": 2,
				"username": "nagore",
				"is_connected": true,
				"is_42": false,
				"avatar": "/media/avatars/default.jpg",
				"friends": []
			}
	  ]

### GET localhost:8000/users/user_list/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
      [
            {
                "username": "jimenetz",
                "is_connected": false,
                "avatar": "/media/avatars/default.jpg",
                "friends": [
                    "carmentxu",
                    "potxoloTheThird"
                ]
            },
            {
                "username": "manoli",
                "is_connected": false,
                "avatar": "/media/avatars/default.jpg",
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


### POST localhost:8000/users/block_user/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Body:
      {
          "block_username": "manoli"
      }

    Return:
      {
          "success": true,
          "message": "w has been blocked."
      }
  ---


### POST localhost:8000/users/unblock_user/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Body:
      {
          "block_username": "manoli"
      }

    Return:
      {
          "success": true,
          "message": "w has been blocked."
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
              "avatar": "/media/avatars/default.jpg",
              "friends": [
                  "ramoncin"
              ]
          },
          {
              "username": "potxolo",
              "is_connected": true,
              "avatar": "/media/avatars/default.jpg",
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
              "avatar": "/media/avatars/default.jpg",
              "friends": [
                  "carmentxu",
                  "potxoloTheThird"
              ]
          },
          "receiver": {
              "username": "manoli",
              "is_connected": true,
              "avatar": "/media/avatars/default.jpg",
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
                    "avatar": "/media/avatars/default.jpg",
                    "friends": [
                        "carmentxu",
                        "potxoloTheThird"
                    ]
                },
                "receiver": {
                    "username": "manoli",
                    "is_connected": true,
                    "avatar": "/media/avatars/default.jpg",
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
                "avatar": "/media/avatars/default.jpg",
                "friends": [
                    "carmentxu",
                    "potxoloTheThird"
                ]
            },
            "receiver": {
                "username": "manoli",
                "is_connected": true,
                "avatar": "/media/avatars/default.jpg",
                "friends": []
            },
            "message_set": []
        }
  ---
  
  ### GET localhost:8000/conversations/check_invitation/

    Authorization required YES

      Headers:
          Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

      Return:
          {
          "chat_invitation": 4
      }
    ---
### POST localhost:8000/conversations/accept_invitation/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
        {
			"initiator": {
				"id": 3,
				"username": "a",
				"email": "",
				"is_connected": true,
				"is_42": false,
				"avatar": null,
				"friends": [
					"b",
					"imontero"
				],
				"chat_invitation": false
			},
			"receiver": {
				"id": 2,
				"username": "imontero",
				"email": "",
				"is_connected": true,
				"is_42": false,
				"avatar": null,
				"friends": [
					"a"
				],
				"chat_invitation": false
			},
			"message_set": []
		}

---
### POST localhost:8000/conversations/decline_invitation/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
		{
			"message": "Invitation declined and conversation deleted"
		}
---





  ### WEBSOCKET ws://localhost:8000/ws/chat/<int:convo_id>/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

  Connect to websocket
  Send/receive message

    Message:
        {"message":"holii"}
---
  ## Chat
---
### POST localhost:8000/blockhain/add/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Body:
      {
          "match_score":"match_id=1 timestamp=3894894898932 player1=pepe player2=manolo winner=pepe"
      }

---
### GET localhost:8000/blockhain/get/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
        [
            {
                "match_id": "1",
                "timestamp": "894894898932",
                "player1": "pepe",
                "player2": "manolo",
                "winner": "pepe"
            },
            {
                "match_id": "2",
                "timestamp": "4353454",
                "player1": "potxolo",
                "player2": "pako",
                "winner": "potxolo"
            }
        ]
---
  ## Tournament
---
  ### GET localhost:8000/tournament/detail/<int:tournament_id>/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
        {
          "id": 12,
          "initiator": "imontero",
          "player1": "imontero",
          "player2": "pepe",
          "player3": "ptxolin",
          "player4": "manolete",
          "game1_id": 14,
          "game2_id": 15,
          "final_game_id": 18,
          "game1_winner": "imontero",
          "game2_winner": "manolete",
          "final_game_winner": "manolete",
          "start_time": "2024-06-29T11:29:43Z",
          "end_time": null
      }

---

### GET localhost:8000/tournament/current/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
        [
          {
              "id": 13,
              "player1": "imontero",
              "player2": "pepe",
              "player3": "maricarmen",
              "player4": "manolete",
              "game1_winner": null,
              "game2_winner": null,
              "final_game_winner": null,
              "start_time": "2024-06-29T15:14:38.186303Z",
              "end_time": null
          },
          {
              "id": 12,
              "player1": "imontero",
              "player2": "pepe",
              "player3": "ptxolin",
              "player4": "manolete",
              "game1_winner": "imontero",
              "game2_winner": "manolete",
              "final_game_winner": "manolete",
              "start_time": "2024-06-29T11:29:43Z",
              "end_time": null
          }
      ]

---

### POST localhost:8000/tournament/create/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Return:
        {
            "id": 16,
            "initiator": "imontero",
            "player1": "imontero",
            "player2": "manolete",
            "player3": "teresa",
            "player4": "ptxolin",
            "game1": 23,
            "game2": 24,
            "start_time": "2024-06-29T16:22:53.790"
        }

---

### POST localhost:8000/tournament/create/

  Authorization required YES

    Headers:
         Authorization: Token 7faff8fe07ef93d56b99a6c7f9e94bfc07d2d3eb

    Body:
        {
                "player1_username": "imontero",
                "player2_username": "manolete",
                "tournament_id": 16
        }
    
    Return:
        {
            "id": 16,
            "initiator": "imontero",
            "player1": "imontero",
            "player2": "manolete",
            "player3": "teresa",
            "player4": "ptxolin",
            "game1": 23,
            "game2": 24,
            "final_game": 30,
            "start_time": "2024-06-29T16:22:53.790Z",
            "end_time": null
        }

---



