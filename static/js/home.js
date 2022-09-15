Vue.component('tracker', {
    props: {
        id: '',
        name: '',
        description: '',
        last_modified: '',
    },

    template:
        `
        <tr>
            <td style="max-width: 30px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                <a v-bind:href="'/summary/'+ id">{{name}}</a>
            </td>
            <td style="max-width: 40px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                {{description}}
            </td>
            <td style="max-width: 22px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                {{last_modified}}
            </td>
            <td>
                <div>
                    <a v-bind:href="'/log/'+ id" class = "btn btn-success" type = "button">+</a>
                </div>
            </td>
            <td>
                <div>
                    <div class="dropdown">
                        <button class="btn btn-warning dropdown-toggle" aria-expanded="false" data-bs-toggle="dropdown" type="button">Action</button>
                        <div class="dropdown-menu">
                            <button @click="updateTracker(id)"class="dropdown-item link-info" type="button"><strong>Update</strong></button>
                            <button @click="removeTracker(id)" class="dropdown-item link-danger" type="button"><strong>Remove</strong></button>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
    `,

    created(){
        if (localStorage.getItem('Authentication-Token') == null){
            window.alert("You are not authorised.\nRedirecting to Login page.")
            window.location.href = '/login'
        }
    },

    methods:{
        async removeTracker(id){
            fetch('/api/tracker/' + id,{
                method: 'delete',
                headers: {
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
            })
            .then((response) => {
                if(response.status == 200){
                    window.location = window.location
                }else if(response.status == 401){}
                else if(response.status == 404){
                    window.alert(response.statusText)
                }else{
                    window.alert("Something went wrong.")
                    vue.userLogout()
                }
            })
        },

        async updateTracker(id){
            window.location.href = "/tracker/update/" + id
        }

    }
})

let vue = new Vue({
    el: "#app",
    delimiters: ['${','}'],
    data(){
        return {
            name: 'User',
            trackers: [],
        }
    },

    methods: {
        async userLogout(){
            let response = await fetch('/api/user/logout', {
                                    method: 'get',
                                    headers: {
                                        'Authentication-Token': localStorage.getItem('Authentication-Token'),
                                    },
                                })
            if (response.status === 200) {
                localStorage.clear()
                window.location.href = '/login';
            }else if (response.status === 401){
                window.alert('You are now authorised.')
                window.location.href = '/login';
            }else if (response.status === 500){
                window.alert('Something went wrong.')
            }else{
                window.alert(response.statusText)
            } 
        },

        async fetchTrackers(){
            await fetch('/api/tracker',{
                method: 'get',
                headers: {
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
            })
            .then((response) => {
                if(response.status == 200){
                    return response.json()
                }else if(response.status == 401){}
                else{
                    window.alert("Something went wrong.")
                    userLogout()
                }
            })
            .then((trackers) => {
                this.trackers = trackers
                this.trackers.sort((a,b) => {
                    if(a.last_modified < b.last_modified){
                        return 1
                    }else{
                        return -1
                    }
                })
            });
        },
    },
    
    created() {
        // Redirect to login page if not authorised
        if (localStorage.getItem('Authentication-Token') == null){
            window.alert("You are not authorised.\nRedirecting to Login page.")
            window.location.href = '/login'
            return
        }

        // Fetching trackers to show in the dashboard.
        this.fetchTrackers()

        // Fetching user details
        fetch('/api/user', {
            method: 'get',
            headers: {
                'Authentication-Token': localStorage.getItem('Authentication-Token'),
            },
        })
        .then((response) => {
            if(response.status == 200){
                return response.json()
            }else if(response.status == 401){}
            else{
                window.alert("Something went wrong.")
                userLogout()
            }
        })
        .then((user) => {
            this.name = user.first_name,
            this.name = this.name + " " + user.last_name
        })
    },
});
