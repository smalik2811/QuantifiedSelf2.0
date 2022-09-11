Vue.component("chart", {
    extends: VueChartJs.Scatter,
    props: {
        labels: null,
        data: null,
    },
    mounted() {
        this.renderChart(
          {
            labels: this.labels,
            datasets: [
              {
                label: "Data One",
                backgroundColor: "#f87979",
                data: this.data,
              },
            ],
          },
          { responsive: true, maintainAspectRatio: false }
        );
    },
  });

Vue.component('log', {
    props: {
        id: '',
        value: '',
        note: '',
        timestamp: '',
    },

    template:
        `
            <tr>
                <td>{{value}}</td>
                <td style="max-width: 22px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{{timestamp}}</td>
                <td style="max-width: 60px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{{note}}</td>
                <td>
                    <div>
                        <div class="dropdown">
                            <button class="btn btn-warning dropdown-toggle" aria-expanded="false" data-bs-toggle="dropdown" type="button">Action</button>
                            <div class="dropdown-menu">
                            <button @click="updateLog(id)"class="dropdown-item link-info" type="button"><strong>Update</strong></button>
                            <button @click="removeLog(id)" class="dropdown-item link-danger" type="button"><strong>Remove</strong></button>
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
        async removeLog(id){
            fetch('/api/log/' + id,{
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

        async updateLog(id){
            window.location.href = "/log/update/" + id
        }

    }
})

let vue = new Vue({
    el: "#app",
    delimiters: ['${','}'],
    data(){
        return {
            name: null,
            labels: [],
            data: [],
            logs: [],
            trackerData: {
                id: null,
                name: null,
                description: null,
            }
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

        async fetchTracker(){
            let uri = window.location.pathname.split("/")
            this.trackerData.id = uri[uri.length - 1]
            await fetch('/api/tracker/' + this.trackerData.id,{
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
            .then((tracker) => {
                this.trackerData.name = tracker.name
                this.trackerData.description = tracker.description
            });
        },

        async fetchLogs(){
    
            await fetch('/api/log',{
                method: 'get',
                headers: {
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                    'trackerid' : this.trackerData.id,
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
            .then((logs) => {
                this.logs = logs
                logs.forEach(element => {
                    this.labels.push(element.timestamp)
                    this.data.push(element.value)
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
        this.fetchTracker()
        this.fetchLogs()
        
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
