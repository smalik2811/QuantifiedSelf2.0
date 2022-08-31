Vue.component('tracker', {
    props: {
        id: '',
        name: '',
        description: '',
        last_modified: 'Never',
    },

    template:
        `
        <div class="card" style="width: 18rem;">
            <div class="card-header ">Last Modified: {{last_modified}} </div>
            <img class="card-img-top w-100 d-block" src="https://picsum.photos/400/300" />
            <div class="card-body">
                <h4 class="card-title">{{name}}</h4>
                <p class="card-text">{{description}}</p>
            </div>
            <div class="card-footer ">
                <button class="btn btn-primary" type="button">Log</button>
                <button class="btn btn-warning" type="button">Update</button>
                <button class="btn btn-danger" type="button">Delete</button>
            </div>
        </div>
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
