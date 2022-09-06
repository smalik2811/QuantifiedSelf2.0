Vue.component('tracker', {
    props: {
        id: '',
        name: '',
        description: '',
        last_modified: 'Never',
    },

    template:
        `
        <tr>
            <td>
                <a href="#">{{name}}</a>
            </td>
            <td>
                {{description}}
            </td>
            <td>
                {{last_modified}}
            </td>
            <td>
                <div>
                    <a href = "#" class = "btn btn-success" type = "button">+</a>
                </div>
            </td>
            <td>
                <div>
                    <div class="dropdown">
                        <button class="btn btn-warning dropdown-toggle" aria-expanded="false" data-bs-toggle="dropdown" type="button">Action</button>
                        <div class="dropdown-menu">
                            <a class="dropdown-item link-info" href="#">Edit</a>
                            <a class="dropdown-item link-danger" href="#">Remove</a>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
    `,

    created(){
        
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
    },
    
    created() {
        // Redirect to login page if not authorised
        if (localStorage.getItem('Authentication-Token') == null){
            window.alert("You are not authorised.\nRedirecting to Login page.")
            window.location.href = '/login'
            return
        }

        // Fetching trackers to show in the dashboard.
        fetch('/api/tracker',{
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
        .then((trackers) => this.trackers = trackers);

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
