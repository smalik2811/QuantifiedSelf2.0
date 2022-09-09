Vue.component('value-component', {    
    template:`
    <div>
        <label class="form-label">Value</label>
        <input
            v-model="trackerValue"
            @input="$emit('sendvalue', trackerValue);"
            class="form-control"
            type="number"/>
    </div>
    `,
    data(){
        return {
            trackerValue: Number,
        }
    },
}) 

let app = new Vue({
    el: "#app",
    delimiters: ['${','}'],
    data(){
        return {
            logData:{
                value: Number,
                note: null,
                timestamp: null,
            },
            userData: {
                name: null,
            },
            trackerData: {
                id: null,
                name: null,
                description: null,
                type: null,
                options: null,
            },

            trackerTypes: {
                "Numerical": 1,
                "Time Duration": 2,
                "Boolean": 3,
                "Multiple Choice": 4,
            },

            misc: {
                tr_type: null,
                options: null
            }
        }
    },

    methods: {
        
        getvalue: function(value){
            this.logData.value = value
        },

        selectType: function(type){
            if (type in this.trackerTypes){
                this.trackerData.type = this.trackerTypes[type]
                this.misc.tr_type = type
                
                if (this.trackerData.type == 4){
                    this.misc.options = "Option1, Option2, Option3"
                }else{
                    this.misc.options = null
                }
            }
        },

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

        async createTracker(){

            if (this.misc.options != null){
                this.trackerData.options = this.misc.options.split(", ")
            }

            fetch('/api/tracker', {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
                body: JSON.stringify(this.trackerData),
            })
            .then((response) => {
                if(response.status == 201){
                    return response.json()
                }else if(response.status == 400){
                    window.alert(response.statusText)
                }else if(response.status == 401){}
                else if(response.status == 409){
                    window.alert(response.statusText)
                }else{
                    window.alert(response.statusText)
                }
                
            })
            .then((data) => 
                {
                    window.location.href = '/';
                })
        }
    },

    computed: {
        multiChoice(){
          return this.trackerData.type === 4
      }
    },

    created() {
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
            this.userData.name = user.first_name,
            this.userData.name = this.userData.name + " " + user.last_name
        })

        // Fetching tracker details
        {
            let uri = window.location.pathname.split("/")
            this.trackerData.id = uri[uri.length - 1]

            fetch('/api/tracker/' + this.trackerData.id, {
                method: 'get',
                headers: {
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
            })
            .then((response) => {
                if(response.status == 200){
                    return response.json()
                }else if(response.status == 400){
                    window.alert(response.statusText)
                }else if(response.status == 401){}
                else if(response.status == 404){
                    window.alert(response.statusText)
                }else{
                    window.alert(response.statusText)
                }  
            })
            .then((data) => 
                {
                    this.trackerData = data
                }
            )
        }
      },
});