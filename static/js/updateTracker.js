new Vue({
    el: "#app",
    delimiters: ['${','}'],
    data(){
        return {
            userData: {
                name: null,
            },
            trackerData: {
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
            
            trackerTypes2: {
                1: "Numerical",
                2: "Time Duration",
                3: "Boolean",
                4: "Multiple Choice"
            },

            misc: {
                tr_name: null,
                tr_type: null,
                options: null
            }
        }
    },

    methods: {

        selectType: function(type){
            if (type in this.trackerTypes){
                this.trackerData.type = this.trackerTypes[type]
                this.misc.tr_type = type
                
                if (this.trackerData.type == 4){
                    this.misc.options = "Option1, Option2, Option3"
                }else{
                    this.misc.options = null
                    this.trackerData.options = null
                }
            }
        },

        selectType2: function(type){
            if (type in this.trackerTypes2){
                this.misc.tr_type = this.trackerTypes2[type]
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

        async updateTracker(){

            if (this.misc.options != null){
                this.trackerData.options = this.misc.options.split(", ")
            }

            fetch('/api/tracker/' + this.misc.tr_name, {
                method: 'patch',
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

        // Fetching tracker data
        {
            let uri = window.location.pathname.split("/")
            this.misc.tr_name = uri[uri.length - 1]

            fetch('/api/tracker/' + this.misc.tr_name, {
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
                    this.selectType2(this.trackerData.type)
                    this.misc.options = ""
                    for (let i = 0; i < this.trackerData.options.length - 1; i ++){
                        this.misc.options += this.trackerData.options[i] + ", "
                    }
                    this.misc.options += this.trackerData.options[this.trackerData.options.length-1]
                }
            )
        }
    },
});