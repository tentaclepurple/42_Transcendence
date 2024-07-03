from .models import Conversation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import MyUser
from users.serializers import UserSerializer
from .serializers import ConversationListSerializer, ConversationSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse, get_object_or_404
from django.http import Http404
from backend.settings import logger



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
    
    if request.user in participant.blocked_users.all():
        return Response({'message': 'You cannot start a conversation with this user because they have blocked you.'}, status=400)
    
    conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                               Q(initiator=participant, receiver=request.user))
    
    if conversation.exists():
        conversation_id = conversation[0].id
        return redirect(reverse('get_conversation', args=(conversation_id,)))
    
    else:
        conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
        participant.chat_invitation = conversation.id
        participant.save()
        return Response({
                    'conversation_id': conversation.id,
                    'initiator': UserSerializer(instance=request.user).data,
                    'receiver': UserSerializer(instance=participant).data                    
        })
    

@api_view(['POST'])
def accept_invitation(request):
    user = request.user
    
    if user.chat_invitation == 0:
        return Response({'message': 'No invitation found'}, status=400)
    
    convo_id = user.chat_invitation
    user.chat_invitation = 0
    user.save()
    logger.warning(f"Conversation ID: {convo_id} and User chat_inv: {user.chat_invitation}")
    return redirect(reverse('get_conversation', args=(convo_id,)))


@api_view(['POST'])
def decline_invitation(request):
    user = request.user
    
    convo_id = user.chat_invitation
    
    try:
        conversation = Conversation.objects.get(id=convo_id)
        conversation.delete()
        user.chat_invitation = 0
        user.save()
        return Response({'message': 'Invitation declined and conversation deleted'})
    except Conversation.DoesNotExist:
        raise Http404("Conversation does not exist")




@api_view(['GET'])
def check_invitation(request):
    user = request.user
    response = {
        'chat_invitation': user.chat_invitation,
        'username': user.username
    }
    return Response(response)



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
