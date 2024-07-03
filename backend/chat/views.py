from django.shortcuts import render
from .models import Conversation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import MyUser
from users.serializers import UserSerializer
from .serializers import ConversationListSerializer, ConversationSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse


@api_view(['POST'])
def start_convo(request, ):
    data = request.data
    username = data.get('username')
    
    if username == request.user.username:
        return Response({'message': 'You cannot chat with yourself'}, status=400)

    try:
        participant = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        return Response({'message': 'You cannot chat with a non existent user'})

    if not participant.is_connected:
        return Response({'message': 'User is not connected'}, status=400)    
    
    conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                               Q(initiator=participant, receiver=request.user))
    
    if conversation.exists():
        conversation_id = conversation[0].id
        return redirect(reverse('get_conversation', args=(conversation_id,)))
    
    else:
        conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
        return Response({
                    'conversation_id': conversation.id,
                    'initiator': UserSerializer(instance=request.user).data,
                    'receiver': UserSerializer(instance=participant).data                    
        })
    

@api_view(['GET'])
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Conversation does not exist'})
    else:
        serializer = ConversationSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['GET'])
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(initiator=request.user) |
                                                    Q(receiver=request.user))
    serializer = ConversationListSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)
