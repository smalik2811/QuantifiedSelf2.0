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
        userLogout(){
            fetch('/user/logout', {
                method: 'get',
                headers: {
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
            })
            .then((response) => 
            {
                localStorage.clear()
                window.location.href = '/login';
            }) 
        },
    },

    created() {
        fetch('/tracker',{
            method: 'get',
            headers: {
                'Authentication-Token': localStorage.getItem('Authentication-Token'),
            },
        })
        .then((resopnse) => resopnse.json())
        .then((trackers) => this.trackers = trackers);

        fetch('/user', {
            method: 'get',
            headers: {
                'Authentication-Token': localStorage.getItem('Authentication-Token'),
            },
        })
        .then((response) => response.json())
        .then((user) => {
            this.name = user.first_name,
            this.name = this.name + " " + user.last_name
        })
      },
});
