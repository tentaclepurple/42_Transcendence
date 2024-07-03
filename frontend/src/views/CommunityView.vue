<template>
    <div>
        <!--main-->
        <b-container fluid>
            <!--upper-->
            <b-row>
                <b-col class="bg-primary text-center">
                    <h2>Community</h2>
                    <p>Chat with our community partners!</p>
                </b-col>
            </b-row>
            <b-alert v-model="showConnnectionnAlert" variant="danger" dismissible @closed="closeConnectionAlert()">
                Unable to connect! Please try again later.
            </b-alert>
            <b-row style="height: 500px">
                <b-col sm="4">
                    <ListUsers></ListUsers>
                </b-col>
                <b-col sm="8">
                    <ChatWindow></ChatWindow>
                </b-col>
            </b-row>
        </b-container>
        
    </div>

</template>

<script>
    import TournamentComponent from '../components/TournamentComponent.vue';
    import ListUsers from '../components/ListUsers.vue';
    import ChatWindow from '../components/ChatWindow.vue';
    import { mapState, mapMutations } from 'vuex';

    export default {
        name: 'CommunityView',
        components: {
            ListUsers,
            TournamentComponent,
            ChatWindow
        },
        computed: {
            ...mapState(['showConnnectionnAlert'])
        },
        methods: {
            ...mapMutations(['setConnAlert']),
            closeConnectionAlert() {
                this.setConnAlert(false);
            }
        }
    }
</script>