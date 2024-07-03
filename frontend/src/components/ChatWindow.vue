<template>
    <div>
		<b-card v-if="showChat" class="chat-container mt-4">
			<h2 class="text-center">Chat with {{ userSelected.username }}</h2>
            <div class="messages">
				<div v-for="message in messages" :key="message.id">
					<p>{{ message.realSender }}: {{ message.text }}</p>
				</div>
			</div>
            <input v-model="newMessage" @keyup.enter="sendMessage">
            <b-button class="mt-2 ml-2" @click="sendMessage">Enviar</b-button>
            <b-button variant="danger" class="mt-2 ml-2" @click="closeChat">Cerrar</b-button>
        </b-card>
    </div>
</template>

<script>
    import { getData, postData } from '@/stores/api';
    import { mapState, mapMutations } from 'vuex';

    export default {
        name: 'ChatWindow',
        
        data() {
            return {
			id : 0,
            socket: null,
			messages: [],
            newMessage: '',
			errorMessage: '',
            showChat: false,
            };
        },
        computed: {
            ...mapState(['userSelected', 'triggerChatSocketInit', 'triggerEnterChat'])
        },
        watch: {
            triggerChatSocketInit: function() {
                if (this.triggerChatSocketInit){
                    this.initChatSocket();
                    this.setTriggerChatSocketInit(false);
                }
            },
            triggerEnterChat: function() {
                if (this.triggerEnterChat){
                    //console.log('triggerEnterChat:: ', this.triggerEnterChat);
                    this.conectChat(this.triggerEnterChat);
                    this.setTriggerEnterChat(false);
                }
            }
        },
        methods: {
            ...mapMutations(['setTriggerChatSocketInit', 'setConnAlert', 'setTriggerEnterChat']),
            closeChat() {
                if (this.socket) {
                    this.socket.close();
                    this.socket = null;
                }
                this.showChat = false;
            },
			sendMessage() {
                if (this.newMessage !== '') {
                    const message = {
                        type: 'chat_message',
                        message: this.newMessage,
                        sender: this.userSelected.username 
                    };
                    this.socket.send(JSON.stringify(message));
					//console.log('Mensaje enviado');
                    this.newMessage = '';
                }
            },
            conectChat(id){
                const token = this.$cookies.get('token_auth');
                const path = import.meta.env.VITE_CHAT_APP_BACKEND_URL + id + "/?token=" + token;
                //console.log("PATH", path);
				try{
                    this.getMessage(id);
                    this.showChat = true;
                    this.socket = new WebSocket(path); // replace with your server URL
                    this.socket.onopen = (event) => {
                        //console.log('WebSocket is open now.');
                        id = id;
                    };
    
                    this.socket.onclose = (event) => {
                        //console.log('WebSocket is closed now.');
                        id = 0;
                    };
    
                    this.socket.onerror = (event) => {
                        //console.error('WebSocket error observed:', event);
                    };
    
                    this.socket.onmessage = (event) => {
                        //console.log('WebSocket message received:', event.data);
                        // You can push the received message to your messages array here
                        this.messages.push(JSON.parse(event.data));
                    };
                } catch (error) {
                    //console.log(error);
                    this.errorMessage = 'An error occurred while connecting to chat';
                }
            },
			async initChatSocket() {
				this.errorMessage = '';
				const token = this.$cookies.get('token_auth');
				const chatUser = { username: this.userSelected.username };
                try{
				const { data, error } = await postData(import.meta.env.VITE_APP_BACKEND_URL + '/conversations/start/', chatUser, {
					headers: { Authorization: `Token ${token}` }
				});
                if (data && data.conversation_id){
                    //console.log(data);
                    //console.log(data.conversation_id);
                    this.conectChat(data.conversation_id);
                }
                else{
                    //console.log('Chat already done', data.conversation_id)
                }
                } catch (error) {
                    //console.log(error);
                    //console.log('asnlaxaw')
                    this.errorMessage = 'An error occurred while creating chat';
                    this.setConnAlert(true);
                }
			},
            async getMessage(id) {
				try {
					const token = this.$cookies.get('token_auth');
					const received = await getData(import.meta.env.VITE_APP_BACKEND_URL + `/conversations/${id}/`, {
					headers: { Authorization: `Token ${token}` }
					});
					const data = received.data;
					this.messages = data.message_set;
					this.messages.reverse();
				} catch (error) {
					//console.log(error);
					this.errorMessage = 'An error occurred while fetching conv messages';
				}
			},
        }
    }
</script>

<style scope>
  .chat-container {
    width: auto;
    height: 500px;
    border: 1px solid #ccc;
    display: flex;
    flex-direction: column;
    padding: 10px;
  }
  .messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 5px;
    border: 1px solid #ccc;
    margin-bottom: 10px;
	height: 300px;
  }
  .input-area {
    display: flex;
  }
  .input-area input {
    flex-grow: 1;
    margin-right: 5px;
  }
</style>